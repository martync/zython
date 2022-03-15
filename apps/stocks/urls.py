from django.urls import re_path
from .views.stocks import StockHomeView, StockIngredientView,\
    StockIngredientAddView, StockIngredientUpdateView, StockIngredientDeleteView


urlpatterns = [
    re_path(r'^$',
        StockHomeView.as_view(),
        name='stock_home'),

    re_path(r'^(?P<ingredient>\w+)/$',
        StockIngredientView.as_view(),
        name='stock_ingredient'),

    re_path(r'^(?P<ingredient>\w+)/add/$',
        StockIngredientAddView.as_view(),
        name='stock_ingredient_add'),

    re_path(r'^(?P<ingredient>\w+)/(?P<pk>\d+)/edit/$',
        StockIngredientUpdateView.as_view(),
        name='stock_ingredient_edit'),

    re_path(r'^(?P<ingredient>\w+)/(?P<pk>\d+)/delete/$',
        StockIngredientDeleteView.as_view(),
        name='stock_ingredient_delete'),

]