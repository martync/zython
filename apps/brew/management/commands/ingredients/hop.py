from django.conf import settings
from brew.models import Hop
from brew.helpers import xml_import
from brew.beer_xml import HOP_FIELDS

def do_import():
    xml_file = "%sapps/brew/fixtures/Hop.xml" % settings.ROOT_PROJECT
    model_class = Hop
    parent_loop = "HOPS"
    item_loop = "HOP"
    xml_import(xml_file, model_class, parent_loop, item_loop, HOP_FIELDS)