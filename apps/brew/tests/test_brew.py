from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from brew.models import *
from public.utils import show_in_browser
from public.utils.testing import AjaxCallsTestCaseBase
import json


class RecipeTest(AjaxCallsTestCaseBase, TestCase):
    fixtures = [
        "initial_data.json"
    ]
    user_info = {'username': 'martyn',
                 'password': 'magicpony',
                 'email': 'martyn@example.com'}
    user2_info = {'username': 'chuck',
                  'password': 'magicpony',
                  'email': 'chuck@example.com'}

    def setUp(self):
        # Set up the main user
        user = User(
            username=self.user_info['username'],
            email=self.user_info['email']
        )
        user.set_password(self.user_info['password'])
        user.save()
        self.user = user

        user2 = User(
            username=self.user2_info['username'],
            email=self.user2_info['email']
        )
        user2.set_password(self.user2_info['password'])
        user2.save()
        self.user2 = user2

        # Main client
        self.client = Client()

        # Set up the main recipe
        style = BeerStyle.objects.filter(name__icontains="Doppelbock")[0]
        self.style = style
        recipe = Recipe(
            user=self.user,
            name="Test Recipe PoneyPoneyPoney",
            batch_size="50.3",
            style=style,
            recipe_type="allgrain",
            private=False,
            efficiency="75",
        )
        recipe.save()
        recipe.update_slug_url()
        self.recipe = recipe

    def get_logged_client(self):
        self.client.login(
            username=self.user_info['username'],
            password=self.user_info['password']
        )
        return self.client

    def i18n_client(self, language="en", client=None):
        if not client:
            client = self.client
        client.post('/i18n/setlang/', {'language': language})
        return client

    def test_1_malt(self):
        malt = Malt.objects.filter(name__icontains="Maris Otter")[0]
        url_addition = reverse(
            'brew_recipe_addingredient', args=[self.recipe.id, "malt"])
        datas = malt.python_dict()["fields"]

        datas.update({
            'amount': "12.5",
            "malt_id": malt.id,
            "color": malt.color
        })

        # Test with anonymous client
        c = Client()
        response = c.post(url_addition, datas)
        self.assertEqual(response.status_code, 302)

        # Test with logged in client
        c = self.get_logged_client()
        response = c.post(url_addition, datas, **self.ajax_post_kwargs())
        self.is_ajax_response_correct(response)

        # Add another caramel malt
        c = self.i18n_client('fr', c)
        datas['amount'] = "2"
        datas['color'] = "150"
        response = c.post(url_addition, datas, **self.ajax_post_kwargs())
        self.is_ajax_response_correct(response)

        # Do we have 2 Malts ?
        self.assertEqual(self.recipe.recipemalt_set.all().count(), 2)
        # We should have an OG > 1.1
        self.assertEqual(float(self.recipe.get_original_gravity()), 1.069)
        # We should have a color > 16EBC
        self.assertEqual(int(self.recipe.get_ebc()), 31)
        # We should have more than 11% alcool, waw!
        self.assertEqual(int(self.recipe.get_abv()), 6)
        # We should have 0 IBU
        self.assertEqual(float(self.recipe.get_ibu()), 0.)

        malts = self.recipe.recipemalt_set.all()
        self.assertEqual(float(malts[0].percent()), 86.2)
        self.assertEqual(float(malts[1].percent()), 13.8)

        # empirical efficiency
        self.assertEqual(self.recipe.compute_empirical_efficiency(50.3, 1.069), 75)
        self.assertEqual(self.recipe.compute_empirical_efficiency(45, 1.055), 53)

        calculator_data = {}
        calculator_data["collected_volume"] = 55.3
        calculator_data["measured_gravity"] = 1.071
        url_efficiency_calculator = reverse(
            'brew_recipe_efficiency_calculator', args=[self.recipe.id, self.recipe.slug_url])
        response = c.post(url_efficiency_calculator, calculator_data)
        result = json.loads(response.content)
        self.assertEqual(result["efficiency"], 85)

        # Clear all malts
        self.recipe.recipemalt_set.all().delete()

    def test_2_hop(self):
        hop = Hop.objects.filter(name__icontains="Styrian")[0]
        url_addition = reverse(
            'brew_recipe_addingredient', args=[self.recipe.id, "hop"])
        datas = {
            'amount': "80.5",
            "boil_time": "45.5",
            "hop_id": hop.id,
            "acid_alpha": hop.acid_alpha,
            "acid_beta": hop.acid_beta,
            "usage": hop.usage,
            "form": hop.form,
            "name": hop.name,
            "origin": hop.origin,
            "hop_type": hop.hop_type,
        }

        # Test with anonymous client
        c = Client()
        response = c.post(url_addition, datas)
        self.assertEqual(response.status_code, 302)

        # Test with logged in client
        c = self.get_logged_client()
        response = c.post(url_addition, datas, **self.ajax_post_kwargs())
        self.is_ajax_response_correct(response)

        # Add aroma hop
        c = self.i18n_client('fr', c)
        datas['boil_time'] = "12"
        response = c.post(url_addition, datas, **self.ajax_post_kwargs())
        self.is_ajax_response_correct(response)

        # Do we have 2 Hops ?
        self.assertEqual(self.recipe.recipehop_set.all().count(), 2)
        # We should have total IBU > 46
        self.assertEqual(float(self.recipe.get_ibu()), 41.9)
        # We should have no color
        self.assertEqual(float(self.recipe.get_ebc()), 0)
        # We should have no alcool :(
        self.assertEqual(float(self.recipe.get_abv()), 0)

        # Clear all hops
        self.recipe.recipehop_set.all().delete()

    def test_3_misc(self):
        misc = Misc.objects.filter(
            name__icontains="Coriander")[0]
        url_addition = reverse(
            'brew_recipe_addingredient', args=[self.recipe.id, "misc"])
        datas = misc.python_dict()["fields"]
        datas.update({
            "amount": "50.5",
            "use_in": "boil",
            "time": "30.5",
            "time_unit": "min",
            "misc_id": misc.id
        })
        # Test with anonymous client
        c = Client()
        response = c.post(url_addition, datas)
        self.assertEqual(response.status_code, 302)

        # Test with logged in client
        c = self.get_logged_client()
        response = c.post(url_addition, datas, **self.ajax_post_kwargs())
        self.is_ajax_response_correct(response)

    def test_4_yeast(self):
        yeast = Yeast.objects.filter(
            product_id__icontains="58")[0]
        url_addition = reverse(
            'brew_recipe_addingredient', args=[self.recipe.id, "yeast"])
        datas = yeast.python_dict()["fields"]
        datas.update({
            "yeast_id": yeast.id
        })
        # Test with anonymous client
        c = Client()
        response = c.post(url_addition, datas)
        self.assertEqual(response.status_code, 302)

        # Test with logged in client
        c = self.get_logged_client()
        response = c.post(url_addition, datas, **self.ajax_post_kwargs())
        self.is_ajax_response_correct(response)

        # Do we have 1 yeast ?
        self.assertEqual(self.recipe.recipeyeast_set.all().count(), 1)

        # Clear all yeasts
        self.recipe.recipeyeast_set.all().delete()

    def test_5_recipe_private(self):
        recipe = self.recipe
        recipe_name = "PoneyPoneyPoney"
        client2 = Client()
        client2.login(
            username=self.user2_info['username'],
            password=self.user2_info['password']
        )
        client_author = Client()
        client_author.login(
            username=self.user_info['username'],
            password=self.user_info['password']
        )

        # Anonymous should see recipe
        response = self.client.get('/')
        self.assertContains(response, recipe_name)

        # Other users should see it too
        response = client2.get('/')
        self.assertContains(response, recipe_name)

        # Recipe author should see it
        response = client_author.get('/')
        self.assertContains(response, recipe_name)

        # Set the recipe to private
        recipe.private = True
        recipe.save()

        # Anonymous shouldn't see this recipe
        response = self.client.get('/')
        self.assertNotContains(response, recipe_name)

        # Other users shouldn't see it
        response = client2.get('/')
        self.assertNotContains(response, recipe_name)

        # Recipe author should see it
        response = client_author.get('/')
        self.assertContains(response, recipe_name)

        # Set the recipe to public
        recipe.private = False
        recipe.save()

    def test_6_recipe_printable(self):
        # Use our logged in client
        client = Client()
        client.login(
            username=self.user_info['username'],
            password=self.user_info['password']
        )

        # Add some malt to get back the ingredient list
        malt = Malt.objects.filter(name__icontains="Maris Otter")[0]
        url_addition = reverse(
            'brew_recipe_addingredient', args=[self.recipe.id, "malt"])
        datas = malt.python_dict()["fields"]
        datas["amount"] = "8"
        c = self.get_logged_client()
        c.post(url_addition, datas)

        # In the detail page, we must have the 'edit_ingredient' link
        recipe = self.recipe
        client.get(reverse("unit_set", args=["volume", "l"]), )
        response = client.get(recipe.get_absolute_url())
        check_string = 'href="/recipe/1/edit/malt/1/"'
        self.assertContains(response, check_string)

        # In the detail page, we do not get the 'edit_ingredient' link
        response = client.get(reverse('brew_recipe_print', args=[recipe.id, recipe.slug_url]))
        self.assertNotContains(response, check_string)

    def test_add_new_recipe(self):
        recipe_name = "test_add_new_recipe"
        self.assertEqual(Recipe.objects.filter(name=recipe_name).count(), 0)
        datas = {
            "batch_size": "12",
            "name": recipe_name,
            "efficiency": "75",
            "recipe_type": "allgrain",
            "recipe_style": "68",
            "private": "on",
            "mash_tun_deadspace": "2.0",
            "boiler_tun_deadspace": "4.0",
            "evaporation_rate": "9",
            "grain_temperature": "22"
        }
        client = self.get_logged_client()

        # Fixed the unit app initialisation crash.
        # We must run 1 request to set every unit preferences
        # in session before using it
        response = client.get("/")
        # .

        response = client.post(reverse("brew_recipe_add"), datas, follow=True)
        self.assertTemplateUsed(response, "brew/recipe_detail.html")
        self.assertEqual(Recipe.objects.filter(name=recipe_name).count(), 1)

    def test_cascade_deletion(self):
        recipe1 = Recipe(
            user=self.user,
            name="Test Recipe PoneyPoneyPoney",
            batch_size="50.3",
            style=self.style,
            recipe_type="allgrain",
            private=False,
            efficiency="75",
        )
        recipe1.save()
        recipe2 = Recipe(
            user=self.user,
            name="Test Clone Recipe",
            batch_size="50.3",
            style=self.style,
            recipe_type="allgrain",
            private=False,
            efficiency="75",
            forked_from=recipe1
        )
        recipe2.save()
        recipe1.delete()
        self.assertEqual(recipe2, Recipe.objects.get(pk=recipe2.pk))

    def test_batch_size_division_zero(self):
        recipe = Recipe(
            user=self.user,
            name="Test Recipe PoneyPoneyPoney",
            batch_size="0",
            style=self.style,
            recipe_type="allgrain",
            private=False,
            efficiency="75",
        )
        recipe.save()
        self.assertEqual(recipe.get_original_gravity(), '1.000')
        self.assertEqual(recipe.compute_empirical_efficiency(50.3, 1.069), 0)

    def test_ingredients_no_duration_typeerror(self):
        hop = Hop.objects.filter(name__icontains="Styrian")[0]
        client = self.get_logged_client()
        url_addition = reverse(
            'brew_recipe_addingredient', args=[self.recipe.id, "hop"])
        durations = ["", "40"]
        for duration in durations:
            datas = {
                'amount': "80.5",
                "boil_time": duration,
                "hop_id": hop.id,
                "acid_alpha": hop.acid_alpha,
                "acid_beta": hop.acid_beta,
                "usage": hop.usage,
                "form": hop.form,
                "name": hop.name,
                "origin": hop.origin,
                "hop_type": hop.hop_type,
            }
            response = client.post(url_addition, datas)
            self.assertEqual(response.status_code, 302)

        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(len(recipe.ingredients()), 2)

    def test_get_as_text(self):
        response = self.client.get(reverse("brew_recipe_print", args=[self.recipe.pk, self.recipe.slug_url]))
        recipe_txt = self.recipe.get_as_text(response.context)
        self.assertIn("Fly sparge with 57.7 l of water at 78.0 c", recipe_txt)
