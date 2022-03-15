from django.conf.urls import patterns, url
from .views.stocks import StockHomeView, StockIngredientView,\
    StockIngredientAddView, StockIngredientUpdateView, StockIngredientDeleteView


urlpatterns = patterns(
    '',

    url(r'^$',
        StockHomeView.as_view(),
        name='stock_home'),

    url(r'^(?P<ingredient>\w+)/$',
        StockIngredientView.as_view(),
        name='stock_ingredient'),

    url(r'^(?P<ingredient>\w+)/add/$',
        StockIngredientAddView.as_view(),
        name='stock_ingredient_add'),

    url(r'^(?P<ingredient>\w+)/(?P<pk>\d+)/edit/$',
        StockIngredientUpdateView.as_view(),
        name='stock_ingredient_edit'),

    url(r'^(?P<ingredient>\w+)/(?P<pk>\d+)/delete/$',
        StockIngredientDeleteView.as_view(),
        name='stock_ingredient_delete'),

)
