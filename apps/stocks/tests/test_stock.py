from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from brew.models import *
from public.utils import show_in_browser
from public.utils.testing import AjaxCallsTestCaseBase

from ..choices import INGREDIENTS_DICT


class StockTest(AjaxCallsTestCaseBase, TestCase):
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
        user = User(
            username=self.user_info['username'],
            email=self.user_info['email']
        )
        user.set_password(self.user_info['password'])
        user.save()
        self.user = user
        self.client = Client()
        self.client.login(username=self.user_info['username'], password=self.user_info['password'])
        self.model_slugs = {
            'malt': Malt,
            'hop': Hop,
            'yeast': Yeast
        }
        self.datas = {
            "malt": {
                'stock_amount': "25.3",
                'name': "Paltest",
                'origin': "Django",
                'malt_type': "grain",
                'potential_gravity': "1.098",
                'color': "4",
                'max_in_batch': "100",
                'notes': ""
            },
            "hop": {
                'stock_amount': "250",
                'name': "Cascade Test",
                'origin': "Django",
                'form': "pellets",
                'hop_type': "bittering",
                'acid_alpha': "15",
                'notes': ""
            },
            "yeast": {
                'stock_amount': "10",
                'name': "Good Ale",
                'laboratory': "Dr Django",
                'product_id': "XX",
                'min_attenuation': "76",
                'max_attenuation': "77",
                'min_temperature': "16",
                'max_temperature': "22",
                'form': "dry",
                'yeast_type': "ale",
                'flocculation': "2",
                'notes': "",
            }
        }

    def test_ingredient_views(self):
        for k in INGREDIENTS_DICT.keys():
            url = reverse("stock_ingredient", args=[k])
            response = self.client.get(url)
            self.assertTemplateUsed(response, "stocks/ingredient.html")
            self.assertContains(response, "Nothing here")

    def post_view_ingredients(self, ingredient_slug):
        datas = self.datas[ingredient_slug]
        url = reverse("stock_ingredient_add", args=[ingredient_slug])
        response = self.client.post(url, datas, **self.ajax_post_kwargs())
        return response

    def test_add_ingredients(self):
        self.client.post('/i18n/setlang/', {'language': "fr"})
        for slug, model_class in self.model_slugs.items():
            self.assertEqual(model_class.objects.all().stocked(self.user).count(), 0)
            response = self.post_view_ingredients(slug)
            self.is_ajax_response_correct(response)
            self.assertEqual(model_class.objects.all().stocked(self.user).count(), 1)

            my_ingredient = model_class.objects.all().stocked(self.user)[0]
            self.assertEqual(float(my_ingredient.stock_amount), float(self.datas[slug]["stock_amount"]))
            response = self.client.get(reverse("stock_ingredient", args=[slug]))
            self.assertTrue(my_ingredient.is_in_stock())
            self.assertContains(response, my_ingredient.stock_repr())

    def test_delete_ingredients(self):
        stocked_hop = Hop(stock_user=self.user, **self.datas["hop"])
        stocked_hop.save()

        recipe = Recipe(
            user=self.user,
            name="Test Recipe PoneyPoneyPoney",
            batch_size="50.3",
            style=BeerStyle.objects.filter(name__icontains="Doppelbock")[0],
            recipe_type="allgrain",
            private=False,
            efficiency="75",
        )
        recipe.save()

        recipe_hop_args = self.datas["hop"].copy()
        del recipe_hop_args["stock_amount"]
        recipe_hop = RecipeHop(hop=stocked_hop, recipe=recipe, amount=10, **recipe_hop_args)
        recipe_hop.save()

        stocked_hop.delete()
        self.assertEqual(recipe_hop, RecipeHop.objects.get(pk=recipe_hop.id))
