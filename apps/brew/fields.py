from django.db import models


__all__ = (
    'GravityField', 'BitternessField',
    'ColorField'
)


class GravityField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        decimal_places = kwargs.pop('decimal_places', 3)
        max_digits = kwargs.pop('max_digits', 4)
        super(GravityField, self).__init__(
            max_digits=max_digits,
            decimal_places=decimal_places,
            *args, **kwargs
        )


class BitternessField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        decimal_places = kwargs.pop('decimal_places', 1)
        max_digits = kwargs.pop('max_digits', 6)
        super(BitternessField, self).__init__(
            max_digits=max_digits,
            decimal_places=decimal_places,
            *args, **kwargs
        )


class ColorField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        decimal_places = kwargs.pop('decimal_places', 1)
        max_digits = kwargs.pop('max_digits', 7)
        super(ColorField, self).__init__(
            max_digits=max_digits,
            decimal_places=decimal_places,
            *args, **kwargs
        )
