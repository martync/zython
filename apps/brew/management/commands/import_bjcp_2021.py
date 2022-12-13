import json
from django.core.management.base import BaseCommand
from units.conversions import srm_to_ebc
from brew.models import BeerStyle


class Command(BaseCommand):
    help = """
        Parse the 2021 JSON styleguide
        provided by
        https://github.com/bjcp-brasil/styleguide-2021
        and create brew.models.BeerStyle datas
    """

    def handle(self, **options):
        f = open('apps/brew/management/commands/bjcp-2021.json')
        data = json.load(f)
        guide = "BJCP 2021"
        i = 0
        BeerStyle.objects.filter(guide=guide).delete()

        for cat in data["styleguide"]["category"]:
            cat_name = cat["name"]
            for subcat in cat["subcategory"]:

                bs = BeerStyle(guide=guide, pk=200 + i)
                bs.name = subcat["name"]
                bs.number = cat["id"]
                bs.sub_number = subcat["id"][-1:]
                bs.category = cat_name

                try:
                    bs.original_gravity_max = subcat["statistics"]["og"]["max"]
                    bs.original_gravity_min = subcat["statistics"]["og"]["min"]
                except KeyError:
                    bs.original_gravity_max = 0
                    bs.original_gravity_min = 0

                try:
                    bs.final_gravity_max = subcat["statistics"]["fg"]["max"]
                    bs.final_gravity_min = subcat["statistics"]["fg"]["min"]
                except KeyError:
                    bs.final_gravity_max = 0
                    bs.final_gravity_min = 0

                try:
                    bs.color_max = srm_to_ebc(subcat["statistics"]["srm"]["max"])
                    bs.color_min = srm_to_ebc(subcat["statistics"]["srm"]["min"])
                except KeyError:
                    bs.color_max = 0
                    bs.color_min = 0

                try:
                    bs.alcohol_max = subcat["statistics"]["abv"]["max"]
                    bs.alcohol_min = subcat["statistics"]["abv"]["min"]
                except KeyError:
                    bs.alcohol_max = 0
                    bs.alcohol_min = 0

                try:
                    bs.bitterness_max = subcat["statistics"]["ibus"]["max"]
                    bs.bitterness_min = subcat["statistics"]["ibus"]["min"]
                except KeyError:
                    bs.bitterness_max = 0
                    bs.bitterness_min = 0

                if "examples" in subcat:
                    bs.examples = ", ".join(subcat["examples"])

                bs.profile = "\n\n".join([subcat["aroma"], subcat["appearance"], subcat["flavor"], subcat["mouthfeel"]])
                bs.ingredients = subcat.get("ingredients", "")
                bs.description = subcat.get("impression", "")

                bs.save()
                i += 1

        f.close()
