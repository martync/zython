from django.conf import settings
from brew.models import Misc
from brew.helpers import xml_import
from brew.beer_xml import MISC_FIELDS

def do_import():
    xml_file = "%sapps/brew/fixtures/Misc.xml" % settings.ROOT_PROJECT
    model_class = Misc
    parent_loop = "MISCS"
    item_loop = "MISC"
    
    xml_import(xml_file, model_class, parent_loop, item_loop, MISC_FIELDS)
