from django.conf.urls import patterns, url
from calculator import views

urlpatterns = patterns(
    '',

    url(r'^$',
        views.CalculatorHomeView.as_view(),
        name='calculator_home'),

    url(r'^raw/abv/$',
        views.ABVView.as_view(),
        name='calculator_abv'),
)
