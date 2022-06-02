from django.urls import re_path
from units import views

urlpatterns = [
    re_path(r'^set/(?P<unit>\w+)/(?P<locale>\w+)/$', views.set_unit, name='unit_set'),

]
