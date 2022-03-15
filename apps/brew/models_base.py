import json
from django.db import models
from django.core import serializers
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .fields import GravityField, ColorField
from .managers import IngredientManager


__all__ = (
    'BaseStockModel',
    'BaseMalt', 'BaseHop', 'BaseYeast', 'BaseMisc',
    'HOP_USAGE_CHOICES', 'HOP_TYPE_CHOICES', 'YEAST_TYPE_CHOICES',
    'YEAST_FORM_CHOICES', 'YEAST_FLOCCULATION_CHOICES', 'MISC_TYPE_CHOICES',
    'MALT_TYPE_CHOICES', 'HOP_FORM_CHOICES'
)

MALT_TYPE_CHOICES = (
    ('grain', _('Grain')),
    ('extract', _('Extract')),
    ('dryextract', _('Dry Extract')),
    ('sugar', _('Sugar'))
)

HOP_USAGE_CHOICES = (
    ('boil', _('Boil')),
    ('dryhop', _('Dry Hop')),
    ('firsthop', _('First Wort')),
    ('latehop', _('Late Hop')),
    ('flameout', _('Flame Out')),
)

HOP_FORM_CHOICES = (
    ('leaf', _("Leaf")),
    ('pellets', _("Pellets")),
    ('plug', _("Plug")),
)

HOP_TYPE_CHOICES = (
    ('bittering', _("Bittering")),
    ('aroma', _("Aroma")),
    ('both', _("Both")),
)

YEAST_TYPE_CHOICES = (
    ('ale', _('Ale')),
    ('lager', _('Lager')),
    ('wine', _('Wine')),
    ('champagne', _('Champagne')),
    ('wheat', _('Wheat'))
)

YEAST_FORM_CHOICES = (
    ('liquid', _('Liquid')),
    ('dry', _('Dry')),
    ('culture', _('Culture'))
)

YEAST_FLOCCULATION_CHOICES = (
    ("1", _('Low')),
    ("2", _('Medium')),
    ("3", _('High')),
    ("4", _('Very high')),
)

MISC_USEIN_CHOICES = (
    ('boil', _('Boil')),
    ('mash', _('Mash')),
    ('primary', _('Primary')),
    ('secondary', _('Secondary')),
    ('bottling', _('Bottling'))
)

MISC_TYPE_CHOICES = (
    ('spice', _('Spice')),
    ('fining', _('Fining')),
    ('herb', _('Herb')),
    ('flavor', _('Flavor')),
    ('other', _('Other'))
)


class BaseIngredientMixin(object):
    def python_dict(self):
        return json.loads(self.json_object())[0]

    def json_object(self):
        json_object = serializers.serialize("json", type(self).objects.filter(pk=self.pk))
        python_object = json.loads(json_object)[0]
        python_object["fields"]["%s_id" % self.cls_name()] = str(self.id)
        return json.dumps([python_object, ])

    def cls_name(self):
        return self.__class__.__name__.lower()


class BaseStockModel(models.Model):
    stock_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    stock_added = models.DateTimeField(null=True, blank=True)

    def is_in_stock(self):
        return self.stock_user is not None and self.stock_amount > 0

    class Meta:
        abstract = True


class BaseMalt(models.Model, BaseIngredientMixin):
    name = models.CharField(_('Name'), max_length=100)
    origin = models.CharField(_('Origin'), max_length=50)
    malt_type = models.CharField(_('Type'), choices=MALT_TYPE_CHOICES, max_length=50)

    # Yield
    potential_gravity = GravityField(_('Potential gravity'), default=1.036)
    malt_yield = models.DecimalField(_('Yield'), max_digits=5, decimal_places=2, help_text="%", default=75)

    # Properties
    color = ColorField(_('Color'), )
    diastatic_power = models.DecimalField(_('Diastatic power'), max_digits=4, decimal_places=1, help_text="Lint.", default=75)
    protein = models.DecimalField(_('Protein'), max_digits=4, decimal_places=1, help_text="%", default=10)
    max_in_batch = models.DecimalField(_('Max in batch'), max_digits=4, decimal_places=1, help_text="%", default=100)
    notes = models.TextField(_('Notes'), blank=True, null=True)

    objects = IngredientManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return _(u"Malt %s") % self.name

    def stock_repr(self):
        return u"%s (%s)" % (
            self.name,
            self.origin
        )

    @property
    def copy_fields(self):
        return (
            'name', 'origin', 'malt_type', 'potential_gravity',
            'malt_yield', 'color', 'diastatic_power', 'protein',
            'max_in_batch', 'notes'
        )


class BaseHop(models.Model, BaseIngredientMixin):
    name = models.CharField(_('Name'), max_length=100)
    origin = models.CharField(_('Origin'), max_length=50)
    usage = models.CharField(_('Usage'), choices=HOP_USAGE_CHOICES, max_length=10)
    form = models.CharField(_('Form'), choices=HOP_FORM_CHOICES, default="leaf", max_length=50)
    hop_type = models.CharField(_('Type'), choices=HOP_TYPE_CHOICES, max_length=50)
    acid_alpha = models.DecimalField(_('Acid alpha'), max_digits=4, decimal_places=2)
    acid_beta = models.DecimalField(_('Acid beta'), max_digits=4, decimal_places=2, default=0)
    notes = models.TextField(_('Notes'), blank=True, null=True)

    objects = IngredientManager()

    def is_dry_hop(self):
        return self.usage == 'dryhop'

    def __unicode__(self):
        return _(u"Hop %s") % self.name

    def stock_repr(self):
        return u"%s %s%% (%s)" % (
            self.name,
            self.acid_alpha,
            self.origin
        )

    class Meta:
        abstract = True


class BaseYeast(models.Model, BaseIngredientMixin):
    name = models.CharField(_('Name'), max_length=100)
    laboratory = models.CharField(_('Lab'), max_length=100)
    product_id = models.CharField(_('Product id'), max_length=100)
    yeast_type = models.CharField(_('Type'), choices=YEAST_TYPE_CHOICES, max_length=50, default="ale")
    form = models.CharField(_('Form'), choices=YEAST_FORM_CHOICES, max_length=50, default="dry")
    flocculation = models.CharField(_('Flocculation'), choices=YEAST_FLOCCULATION_CHOICES, max_length=50, default="2")
    min_attenuation = models.DecimalField(_('Min attenuation'), max_digits=5, decimal_places=2, default=72)
    max_attenuation = models.DecimalField(_('Max attenuation'), max_digits=5, decimal_places=2, default=73)
    min_temperature = models.DecimalField(_('Min temperature'), max_digits=4, decimal_places=1, default=15)
    max_temperature = models.DecimalField(_('Max temperature'), max_digits=4, decimal_places=1, default=25)
    best_for = models.TextField(_('Best for'), null=True, blank=True)
    notes = models.TextField(_('Notes'), null=True, blank=True)

    objects = IngredientManager()

    def __unicode__(self):
        return _(u"Yeast %s") % self.name

    def stock_repr(self):
        return u"%s %s %s (%s)" % (
            self.name,
            self.laboratory,
            self.product_id,
            self.get_form_display()
        )

    def attenuation(self):
        return (self.min_attenuation + self.max_attenuation) / 2

    class Meta:
        abstract = True


class BaseMisc(models.Model, BaseIngredientMixin):
    name = models.CharField(_('Name'), max_length=100)
    misc_type = models.CharField(_('Type'), choices=MISC_TYPE_CHOICES, max_length=50)
    usage = models.CharField(_("Usage"), max_length=100, blank=True, null=True)
    use_in = models.CharField(_('Use for'), choices=MISC_USEIN_CHOICES, default="boil", max_length=50)
    notes = models.TextField(_('Notes'), null=True, blank=True)

    def __unicode__(self):
        return _(u"Misc %s") % self.name

    class Meta:
        abstract = True
