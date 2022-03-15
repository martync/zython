from datetime import datetime
from django import forms
from units.forms import UnitModelForm
from brew.utils.forms import BS3FormMixin
from brew.models import Malt, Hop, Yeast


class BaseStockFormMixin(object):
    def save(self, *args, **kwargs):
        if not self.instance.id:
            self.instance.stock_added = datetime.now()
        return super(BaseStockFormMixin, self).save(*args, **kwargs)


class StockMaltForm(BaseStockFormMixin, BS3FormMixin, UnitModelForm):
    unit_fields = {'weight': ['stock_amount', ], 'color': ['color', ]}

    class Meta:
        model = Malt
        fields = (
            'stock_amount', 'name', 'origin', 'malt_type',
            'potential_gravity', 'color', 'max_in_batch', 'notes'
        )


class StockHopForm(BaseStockFormMixin, BS3FormMixin, UnitModelForm):
    unit_fields = {'hop': ['stock_amount', ]}

    class Meta:
        model = Hop
        fields = (
            'stock_amount', 'name', 'origin', 'form',
            'hop_type', 'acid_alpha', 'notes',
        )


class StockYeastForm(BaseStockFormMixin, BS3FormMixin, forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(StockYeastForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Yeast
        fields = (
            'stock_amount', 'name', 'laboratory',
            'product_id', 'min_attenuation', 'max_attenuation',
            'min_temperature', 'max_temperature',
            'form',
            'yeast_type', 'flocculation',
            'notes',
        )
