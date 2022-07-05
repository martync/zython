import math
import random
from operator import itemgetter
from datetime import datetime
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_comments.signals import comment_was_posted
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.urls import reverse
from public.helpers import send_email_html
from units.conversions import kg_to_lb, ebc_to_srm, \
    srm_to_ebc, l_to_gal, g_to_oz, f_to_c, c_to_f

from .fields import BitternessField, GravityField, ColorField
from .models_base import *
from . import formulas
from .managers import RecipeManager
from . import settings as app_settings


__all__ = (
    'RECIPE_TYPE_CHOICES', 'MISC_TIME_CHOICES',
    'MASH_TYPE_CHOICES', 'BeerStyle', 'Recipe',
    'Malt', 'Hop', 'Misc', 'Yeast',
    'RecipeMalt', 'RecipeHop', 'RecipeMisc', 'RecipeYeast',
    'MashStep'
)

RECIPE_TYPE_CHOICES = (
    ('allgrain', _("All grain")),
    ('partial', _("Partial mash")),
    ('extract', _("Extract")),
    ('adjunct', _("Adjunct")),
    ('sugar', _("Sugar"))
)

MISC_TIME_CHOICES = (
    ('min', _('Mins')),
    ('hours', _('Hours')),
    ('days', _('Days')),
    ('weeks', _('Weeks'))
)

MASH_TYPE_CHOICES = (
    ('infusion', _('Infusion')),
    ('decoction', _('Decoction')),
    ('temperature', _('Temperature'))
)


class BeerStyle(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    guide = models.CharField(max_length=200)
    number = models.IntegerField()
    sub_number = models.CharField(max_length=1)

    # Ranges
    original_gravity_min = GravityField()
    original_gravity_max = GravityField()
    final_gravity_min = GravityField()
    final_gravity_max = GravityField()
    bitterness_min = BitternessField()
    bitterness_max = BitternessField()
    color_min = ColorField()
    color_max = ColorField()
    alcohol_min = models.DecimalField(max_digits=4, decimal_places=2)
    alcohol_max = models.DecimalField(max_digits=4, decimal_places=2)

    # Notes
    description = models.TextField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    examples = models.TextField(blank=True, null=True)

    def get_slug(self):
        return u"%s" % slugify(self.name)

    def get_number(self):
        return "%s.%s" % (self.number, self.sub_number)

    def __str__(self):
        return "%s - %s" % (self.get_number(), self.name)

    def get_absolute_url(self):
        return reverse('brew_style_detail', args=[self.id])

    def og_range(self):
        return [self.original_gravity_min, self.original_gravity_max]

    def fg_range(self):
        return [self.final_gravity_min, self.final_gravity_max]

    def ibu_range(self):
        return [self.bitterness_min, self.bitterness_max]

    def color_range(self):
        return [self.color_min, self.color_max]

    def alcohol_range(self):
        return [self.alcohol_min, self.alcohol_max]

    class Meta:
        ordering = ('number', 'sub_number')


class Recipe(models.Model):
    """
    The main beer recipe
    """
    name = models.CharField(_('Name'), max_length=100)
    slug_url = models.SlugField(null=True, blank=True, default="zython")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, blank=True)
    batch_size = models.DecimalField(_('Batch size'), max_digits=8, decimal_places=1, help_text="L")
    style = models.ForeignKey('BeerStyle', verbose_name=_('Style'), blank=True, null=True, on_delete=models.SET_NULL)
    recipe_type = models.CharField(_('Type'), choices=RECIPE_TYPE_CHOICES, default="allgrain", max_length=50)
    mes_original_gravity = GravityField(null=True, blank=True)
    mes_final_gravity = GravityField(null=True, blank=True)
    mes_alcohol = models.DecimalField(max_digits=3, decimal_places=1, default="0.0")

    # - - -
    # Preferences
    private = models.BooleanField(_(u'Private recipe ?'), default=False, help_text=_(u"If checked, this recipe will not be listed to other users."))
    notes = models.TextField(_('Notes'), null=True, blank=True)
    efficiency = models.DecimalField(_('Efficiency'), max_digits=4, decimal_places=1, default="75", help_text="%")
    mash_tun_deadspace = models.DecimalField(_('Mash tun deadspace'), max_digits=7, decimal_places=1, help_text="L", default="1.5")
    boiler_tun_deadspace = models.DecimalField(_('Boiler tun deadspace'), max_digits=7, decimal_places=1, help_text="L", default="1.5")
    evaporation_rate = models.DecimalField(_('Evaporation rate'), max_digits=5, decimal_places=2, help_text="%", default="8")
    grain_temperature = models.DecimalField(_('Grain temperature'), max_digits=3, decimal_places=1, default="22")
    forked_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    last_destock_datetime = models.DateTimeField(null=True, blank=True)

    objects = RecipeManager()

    # - - -
    # Generic model class/methods

    def update_slug_url(self):
        self.slug_url = slugify(u"%s" % self.name)[:49]
        self.save()

    def can_be_viewed_by_user(self, user):
        if self.private and user != self.user and not user.has_perm('brew.view_recipe', self):
            return False
        else:
            return True

    def clone_to_user(self, user):
        this_recipe = Recipe.objects.get(pk=self.pk)
        new_recipe = self
        new_recipe.pk = None
        new_recipe.user = user
        new_recipe.forked_from = this_recipe
        new_recipe.last_destock_datetime = None
        new_recipe.save()
        reversed_relations = ("recipemalt_set", "recipehop_set", "recipeyeast_set", "mashstep_set", "recipemisc_set")
        for rel in reversed_relations:
            children = getattr(this_recipe, rel).all()
            for child in children:
                child.pk = None
                child.recipe = new_recipe
                child.save()
        return new_recipe

    def guess_style(self):
        """
        According to the OG, FG, ABV, IBU and EBC,
        will return a queryset of corresponding Style
        """
        og = self.get_original_gravity()
        fg = self.get_final_gravity()
        abv = self.get_abv()
        ibu = self.get_ibu()
        ebc = self.get_ebc()
        return BeerStyle.objects.filter(
            original_gravity_min__lte=og,
            original_gravity_max__gte=og,
            final_gravity_min__lte=fg,
            final_gravity_max__gte=fg,
            alcohol_min__lte=abv,
            alcohol_max__gte=abv,
            bitterness_min__lte=ibu,
            bitterness_max__gte=ibu,
            color_min__lte=ebc,
            color_max__gte=ebc,
        )

    def zython_advice_color(self):
        ebc = self.get_ebc()
        advices = []
        if ebc < 3:
            advices = [
                _(u"Looks so clear !!"),
                _(u"This beer makes me thirsty, almost transparent :)"),
                _(u"A brighter beer will be invisible"),
            ]
        elif ebc < 10:
            advices = [
                _(u"I love blonds !!"),
                _(u"A regular blond beer"),
                _(u"This color is fine"),
            ]
        elif ebc < 20:
            advices = [
                _(u"Looks like gold, good job !"),
                _(u"A fresh light-amber, yummy"),
                _(u"This beer looks serious, gold !"),
            ]
        elif ebc < 30:
            advices = [
                _(u"This beer has a great amber color"),
                _(u"A fresh dark-amber, sooo yummy"),
                _(u"This color is perfect for dark ambers"),
            ]
        elif ebc < 50:
            advices = [
                _(u"Yeaahh, a brown beer"),
                _(u"Nice job, this beer is not that dark, just great !"),
                _(u"Someone just made a prefect brown beer"),
            ]
        elif ebc < 100:
            advices = [
                _(u"That's pretty dark"),
                _(u"We can't anything see through this beer excepting the fact that it looks dark"),
                _(u"Black, perfectly black."),
            ]
        elif ebc >= 100:
            advices = [
                _(u"An oil well"),
                _(u"Are you sure this beer should be that dark ?"),
                _(u"Am I blind or this beer is black ?")
            ]
        if advices:
            return random.choice(advices)
        else:
            return ""

    @property
    def cache_key(self):
        # TODO:
        # I consider modifying the cache_key system to have a unique
        # key each time the object is saved.
        modified = self.modified or datetime.now()
        return "%s_%s" % (self.id, modified.strftime('%Y%m%d%H%M%S%f'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brew_recipe_detail', args=(str(self.id), self.slug_url))

    class Meta:
        ordering = ('-created',)
        # permissions = (
        #     ('view_recipe', _(u'View recipe')),
        # )

    # - - -
    # Water volumes

    def water_initial_mash(self):
        """The estimated good ration grain/water"""
        ratio = float(app_settings.WATER_L_PER_GRAIN_KG)
        grain = float(self.get_total_grain())
        return ratio * grain

    def water_boiloff(self):
        """Volume of water lost due to boiloff/evaporation"""
        volume = float(self.batch_size + self.boiler_tun_deadspace)
        boil_time = float(self.get_boil_time() + 3) / 60.
        boil_off = volume * (float(self.evaporation_rate) / 100.) * boil_time
        return boil_off

    def water_mash_added(self):
        """Sum of the water added during mash process"""
        steps = self.mashstep_set.all()
        if steps.count():
            return float(steps.aggregate(Sum('water_added')).get('water_added__sum'))
        return float(self.water_initial_mash())

    def water_grain_absorbtion(self):
        """Total amount of water lost due to grain absorbtion"""
        grain_absorbtion = float(self.get_total_grain({'malt_type': 'grain'})) * 1.001
        return grain_absorbtion

    def boil_size(self):
        """The estimated water volume before boiling"""
        return self.water_boiloff() + float(self.batch_size) + float(self.boiler_tun_deadspace)

    def extra_water_added(self):
        """Volume of wort coming from sugar/extract"""
        # 1 kg sugar == 0,55 L added
        # TODO : adjust this index for dry/extracts
        total = 0.
        sugar_index = 0.55
        total += float(self.get_total_grain({'malt_type__in': ['sugar', 'extract', 'dryextract']})) * sugar_index
        return total

    def water_sparge(self):
        """Calculated volume of sparge water"""
        water_sparge = self.boil_size()
        water_sparge += float(self.mash_tun_deadspace)
        water_sparge += float(self.water_grain_absorbtion())
        water_mash = float(self.water_mash_added())
        water_sparge -= water_mash
        water_sparge -= float(self.extra_water_added())
        return water_sparge

    # - - -
    # Mash

    def get_total_grain(self, qs_kwargs={}):
        """Return the weight in kg of all the grains. """
        qs = self.recipemalt_set.filter(**qs_kwargs)
        total = sum(qs.values_list('amount', flat=True))
        return total

    def get_preboil_gravity(self):
        batch_size = l_to_gal(float(self.batch_size) + float(self.water_boiloff()) + float(self.boiler_tun_deadspace))
        return self.get_original_gravity(cache_key="_pbg", batch_size=batch_size)

    def _get_potential_gravity(self, batch_size):
        points = []
        if not batch_size:
            batch_size = l_to_gal(self.batch_size)
        if not batch_size:
            return 0.
        for grain in self.recipemalt_set.all():
            pounds = kg_to_lb(float(grain.amount))
            gravity = float(grain.potential_gravity - 1) * 1000.
            points.append(float(pounds) * float(gravity))
        return (float(sum(points)) / float(batch_size)) / 1000.

    def get_original_gravity(self, cache_key="_og", batch_size=None):
        cache_key = "%s%s" % (self.cache_key, cache_key)
        og = cache.get(cache_key)
        if og is None:
            efficiency = float(self.efficiency) / 100.0
            og = self._get_potential_gravity(batch_size) * efficiency + 1
            cache.set(cache_key, og, 60 * 15)
        return "%.3f" % og

    def compute_empirical_efficiency(self, collected_volume, measured_og):
        """ returns the empirical efficiency in % based on collected volume (L),
            and measured OG (specific gravity). In order to estimate your brewhouse efficiency on that particular recipe.. """
        pot_gravity = self._get_potential_gravity(l_to_gal(collected_volume))
        efficiency = 0
        if pot_gravity > 0:
            efficiency = (measured_og - 1.) / pot_gravity
        return int(efficiency * 100)

    def get_total_mash_time(self):
        time = 0
        for mashstep in self.mashstep_set.all():
            time += mashstep.step_time
            time += mashstep.rise_time
        return time

    def get_mash_schedule(self):
        data = []
        time = 0
        data.append([time, 22])
        for mashstep in self.mashstep_set.all():
            # data.append([time, int(mashstep.temperature)])
            time += mashstep.rise_time
            data.append([int(time), int(mashstep.temperature)])
            time += mashstep.step_time
            data.append([int(time), int(mashstep.temperature)])

        return data

    # - - -
    # Coloration

    @property
    def color_image(self):
        srm = int(self.get_srm())
        if srm > 30:
            srm = 30
        return srm

    def get_srm(self):
        cache_key = "%s_get_srm" % self.cache_key
        recipe_srm = cache.get(cache_key)
        if recipe_srm is None:
            grain_srm = []
            batch_size = l_to_gal(float(self.batch_size))
            if not batch_size:
                return 0.
            for grain in self.recipemalt_set.all():
                pounds = kg_to_lb(float(grain.amount))
                lovibond = ebc_to_srm(float(grain.color))
                grain_srm.append(float(lovibond * pounds) / float(batch_size))
            recipe_mcu = float(sum(grain_srm))
            recipe_srm = 1.4922 * (recipe_mcu ** 0.6859)
            cache.set(cache_key, recipe_srm, 60 * 15)
        return float(recipe_srm.real)

    def get_ebc(self):
        return srm_to_ebc(self.get_srm())

    def get_hex(self):
        try:
            return app_settings.SRM_TO_HEX[str(int(self.get_srm()))]
        except KeyError:
            return "#000000"

    # - - -
    # Bitterness and spices

    def get_boil_time(self):
        cache_key = "%s_boil_time" % self.cache_key
        boil_time = cache.get(cache_key)
        if boil_time is None:
            hops = self.recipehop_set.all()
            if hops.count():
                boil_time = float(hops[0].boil_time or 0)
            else:
                boil_time = 60.0
            cache.set(cache_key, boil_time, 60 * 15)
        return boil_time

    def get_ibu(self):
        cache_key = "%s_ibu" % self.cache_key
        ibu = cache.get(cache_key)
        if ibu is None:
            ibu = 0
            for hop in self.recipehop_set.all():
                ibu += hop.ibu()
            cache.set(cache_key, ibu, 60 * 15)
        return "%.1f" % ibu

    # - - -
    # After fermentation

    def get_final_gravity(self):
        cache_key = "%s_fg" % self.cache_key
        fg = cache.get(cache_key)
        if fg is None:
            gravity = (float(float(self.get_original_gravity()) - 1.) * 1000)
            attenuation = 0.75
            yeasts = self.recipeyeast_set.all()
            if yeasts.count():
                yeast = yeasts[0]
                attenuation = float(yeast.attenuation() / 100)
            fg = ((gravity - (attenuation * gravity)) / 1000) + 1
            cache.set(cache_key, fg, 60 * 15)
        return "%.3f" % fg

    def get_abv(self):
        og = float(self.get_original_gravity())
        fg = float(self.get_final_gravity())
        return formulas.get_abv(og, fg)

    # - - -
    # Ingredients
    def ingredients(self):
        cache_key = "%s_ingredients" % self.cache_key
        ingredients = cache.get(cache_key)
        if ingredients is None:
            ingredients = []
            # -- Mash --
            mash_malt = self.recipemalt_set.all()
            mash_misc = self.recipemisc_set.filter(use_in="mash")
            mash = []
            for malt in mash_malt:
                mash.append({'object': malt, 'weight': malt.amount * 1000})
            for misc in mash_misc:
                mash.append({'object': misc, 'weight': misc.amount})
            recipe_mash = sorted(mash, key=itemgetter('weight'), reverse=True)
            for rm in recipe_mash:
                ingredients.append(rm.get('object'))

            # -- Boil --
            boil_hops = self.recipehop_set.exclude(usage="dryhop")
            boil_misc = self.recipemisc_set.filter(use_in="boil")
            boil = []
            for hop in boil_hops:
                boil.append({'object': hop, 'duration': hop.get_duration()})
            for misc in boil_misc:
                boil.append({'object': misc, 'duration': misc.get_duration()})
            recipe_boil = sorted(boil, key=itemgetter('duration'), reverse=True)
            for rb in recipe_boil:
                ingredients.append(rb.get('object'))

            # -- Late -- and Fermentables
            late_hops = self.recipehop_set.filter(usage="dryhop")
            late_misc = self.recipemisc_set.exclude(use_in__in=["boil", "mash", "bottling", "latehop"])
            late = []
            for hop in late_hops:
                late.append({'object': hop, 'duration': hop.get_duration()})
            for misc in late_misc:
                late.append({'object': misc, 'duration': misc.get_duration()})
            recipe_late = sorted(late, key=itemgetter('duration'), reverse=True)
            for rl in recipe_late:
                ingredients.append(rl.get('object'))

            for ry in self.recipeyeast_set.all():
                ingredients.append(ry)

            for rmb in self.recipemisc_set.filter(use_in="bottling"):
                ingredients.append(rmb)
            cache.set(cache_key, ingredients, 60 * 15)
        return ingredients

    # - - - -
    # Style Controls

    def style_control_ibu(self):
        ibus = float(self.get_ibu())
        if ibus < float(self.style.bitterness_min):
            return _(u"Bitterness is too low")
        elif ibus > float(self.style.bitterness_max):
            return _(u"Bitterness is too high")

    def style_control_og(self):
        og = float(self.get_original_gravity())
        if og < float(self.style.original_gravity_min):
            return _(u"Original gravity is too low")
        elif og > float(self.style.original_gravity_max):
            return _(u"Original gravity is too high")

    def style_control_fg(self):
        fg = float(self.get_final_gravity())
        if fg < float(self.style.final_gravity_min):
            return _(u"Final gravity is too low")
        elif fg > float(self.style.final_gravity_max):
            return _(u"Final gravity is too high")

    def style_control_abv(self):
        abv = float(self.get_abv())
        if abv < float(self.style.alcohol_min):
            return _(u"Alcohol is too low")
        elif abv > float(self.style.alcohol_max):
            return _(u"Alcohol is too high")

    def style_control_color(self):
        color = float(self.get_ebc())
        if color < float(self.style.color_min):
            return _(u"The beer color seems too bright")
        elif color > float(self.style.color_max):
            return _(u"The beer color seems too dark")

    # - - -
    # Stock

    def get_stocked_recipemalts(self):
        return self.recipemalt_set.filter(malt__stock_user=self.user)

    def get_stocked_recipehops(self):
        return self.recipehop_set.filter(hop__stock_user=self.user)

    def get_stocked_recipeyeasts(self):
        return self.recipeyeast_set.filter(yeast__stock_user=self.user)

    def has_stock_ingredients(self):
        """Return True is some ingredients
        used in this recipe come from the
        user stock"""
        # Looks a bit weird but these queries are expensive.
        # we should return True ASAP
        if self.get_stocked_recipemalts():
            return True
        if self.get_stocked_recipehops():
            return True
        if self.get_stocked_recipeyeasts():
            return True
        return False

    def get_as_text(self, extra_context=None):
        context = {"object": self}
        if extra_context:
            context.update(extra_context)
        return render_to_string("brew/recipe_detail.txt", context)


class Malt(BaseStockModel, BaseMalt):
    stock_amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="kg", null=True, blank=True)
    stock_units = "weight"


class Hop(BaseStockModel, BaseHop):
    stock_amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="g", null=True, blank=True)
    stock_units = "hop"


class Yeast(BaseStockModel, BaseYeast):
    stock_amount = models.IntegerField(help_text="units", null=True, blank=True)
    stock_units = "unit"


class Misc(BaseMisc):
    pass


class UpdateRecipeModel(object):
    def save(self, *args, **kwargs):
        resp = super(UpdateRecipeModel, self).save(*args, **kwargs)
        # Save the recipe so that the cache_key is updated
        # The save() method is listened by `reversion`
        # and we don't create a diff for the recipe, but the ingredient
        Recipe.objects.filter(pk=self.recipe.id).update(modified=datetime.now())
        return resp

    def delete(self, *args, **kwargs):
        resp = super(UpdateRecipeModel, self).delete(*args, **kwargs)
        # Save the recipe so that the cache_key is updated
        # The save() method is listened by `reversion`
        # and we don't create a diff for the recipe, but the ingredient
        Recipe.objects.filter(pk=self.recipe.id).update(modified=datetime.now())
        return resp


class RecipeMalt(UpdateRecipeModel, BaseMalt):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="kg")
    malt = models.ForeignKey(Malt, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-amount', 'pk')

    def percent(self):
        total = float(self.recipe.get_total_grain())
        if not total:
            return 0
        return "%.1f" % ((float(self.amount) / total) * 100.)


class RecipeHop(UpdateRecipeModel, BaseHop):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="g")
    boil_time = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    dry_days = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    hop = models.ForeignKey(Hop, null=True, blank=True, on_delete=models.SET_NULL)

    def unit_time(self):
        if self.usage == "dryhop":
            return _("%s days") % self.dry_days
        else:
            return "%s min" % self.boil_time

    def get_duration(self):
        # Duration in minutes
        if self.usage == "dryhop":
            return (self.dry_days or 1) * 24 * 60
        else:
            return self.boil_time or 0

    def ibu(self):
        if self.usage == "dryhop":
            return 0
        elif not self.boil_time:
            return 0
        volume = float(l_to_gal(self.recipe.batch_size))
        gravity = float(self.recipe.get_original_gravity()) - 1
        alpha = float(float(self.acid_alpha) / 100)
        mass = float(g_to_oz(self.amount))
        time = float(self.boil_time)
        mgperl = alpha * mass * 7490 / volume
        util = 1.65 * (math.pow(0.000125, gravity)) * (1 - math.exp(-0.04 * time)) / 4.15
        ibu = mgperl * util
        if self.form == "pellets":
            ibu += ibu * 0.105
        if self.usage == "firsthop":
            ibu += ibu * 0.105
        return ibu

    def save(self, *args, **kwargs):
        # Quick patch for issue #4
        # https://bitbucket.org/m_clement/zython/issue/4/
        if self.is_dry_hop() and not self.dry_days and self.boil_time:
            self.dry_days = float(self.boil_time) / 60 / 24
            self.boil_time = None
        return super(RecipeHop, self).save()


class RecipeYeast(UpdateRecipeModel, BaseYeast):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    yeast = models.ForeignKey(Yeast, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def amount(self):
        # Used for stock compatibility
        return 1


class RecipeMisc(UpdateRecipeModel, BaseMisc):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="g")
    time = models.DecimalField(max_digits=10, decimal_places=1)
    time_unit = models.CharField(choices=MISC_TIME_CHOICES, default="mins", max_length=50)

    def get_duration(self):
        # Duration in minutes
        duration = self.time or 0
        if self.time_unit == 'hours':
            return duration * 60
        elif self.time_unit == 'days':
            return duration * 24 * 60
        elif self.time_unit == 'weeks':
            return duration * 7 * 24 * 60
        else:
            return duration


class MashStep(UpdateRecipeModel, models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ordering = models.IntegerField(default=0)
    name = models.CharField(_("Name"), max_length=100)
    step_type = models.CharField(_("Step type"), choices=MASH_TYPE_CHOICES, max_length=50)
    temperature = models.DecimalField(_("Temperature"), max_digits=4, decimal_places=1)
    step_time = models.IntegerField(_("Step time"), help_text=_("min"))
    rise_time = models.IntegerField(_("Rise time"), help_text=_("min"))
    water_added = models.DecimalField(_("Water added"), max_digits=8, decimal_places=2)

    def initial_heat(self):
        # TODO :
        # Why this doesn't work properly
        # with total grain weight ??
        # Equation doc : http://www.byo.com/stories/techniques/article/indices/45-mashing/631-feel-the-mash-heat

        Hm = 0.3822  # heat capacity of malt
        Hw = 1.0  # heat capacity of water
        Tmt = 74  # temperature of dry malt
        Tma = float(c_to_f(float(self.temperature)))  # temperature of mash step
        M = float(kg_to_lb(self.recipe.get_total_grain()))  # weight of malt in lbs
        if M == 0.0:
            M = 1.
        W = float(float(l_to_gal(self.water_added)) * M)  # weight of water
        if W == 0:
            temp = self.temperature
        else:
            temp = f_to_c(((M * Hm * (Tma - Tmt)) / (W * Hw)) + Tma)
        return temp

    @property
    def is_first_step(self):
        "Is it the first mash step of the recipe ?"
        try:
            return self == self.recipe.mashstep_set.all()[0]
        except IndexError:
            # If no mashtep set yet, it's the first
            return True

    def set_order(self, direction):
        pass

    class Meta:
        ordering = ['ordering', ]


# Signal stuffs
def comment_notification(sender, comment, request, *args, **kwargs):
    if comment.content_type == ContentType.objects.get_for_model(Recipe):
        context = {'comment': comment, 'recipe': comment.content_object}
        subject = _(u"New comment posted")
        from_email = settings.DEFAULT_FROM_EMAIL
        template_name = "brew/email/recipe_comment_posted.html"
        to = []
        if comment.content_object.user != request.user:
            to = [comment.content_object.user.email, ]
            context['recipe_author'] = False
        else:
            to = list(
                User.objects.filter(
                    comment_comments__object_pk=comment.object_pk,
                    comment_comments__content_type=comment.content_type,
                    comment_comments__is_removed=False
                ).exclude(
                    id=request.user.id
                ).distinct().values_list('email', flat=True)
            )
            context['recipe_author'] = True
        if to:
            send_email_html(subject, from_email, to, template_name, context=context)
comment_was_posted.connect(comment_notification)
