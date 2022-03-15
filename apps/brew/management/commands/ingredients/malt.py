from django.conf import settings
from brew.models import Malt
from brew.helpers import xml_import
from brew.beer_xml import FERMENTABLE_FIELDS

def do_import():
    xml_file = "%sapps/brew/fixtures/Grain.xml" % settings.ROOT_PROJECT
    model_class = Malt
    parent_loop = "FERMENTABLES"
    item_loop = "FERMENTABLE"
    xml_import(xml_file, model_class, parent_loop, item_loop, FERMENTABLE_FIELDS)
