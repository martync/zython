from django.conf import settings
from brew.models import BeerStyle
from brew.helpers import xml_import
from brew.beer_xml import STYLE_FIELDS

def do_import():
    xml_file = "%sapps/brew/fixtures/Style.xml" % settings.ROOT_PROJECT
    model_class = BeerStyle
    parent_loop = "STYLES"
    item_loop = "STYLE"
    xml_import(xml_file, model_class, parent_loop, item_loop, STYLE_FIELDS)

