from django.conf import settings
from brew.models import Yeast
from brew.helpers import xml_import
from brew.beer_xml import YEAST_FIELDS

def do_import():
    xml_file = "%sapps/brew/fixtures/Yeast.xml" % settings.ROOT_PROJECT
    model_class = Yeast
    parent_loop = "YEASTS"
    item_loop = "YEAST"
    xml_import(xml_file, model_class, parent_loop, item_loop, YEAST_FIELDS)

