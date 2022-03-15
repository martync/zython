from django.urls import re_path
from calculator import views

urlpatterns = [
    re_path(r'^$',
        views.CalculatorHomeView.as_view(),
        name='calculator_home'),

    re_path(r'^raw/abv/$',
        views.ABVView.as_view(),
        name='calculator_abv'),
]
