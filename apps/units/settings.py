from django.utils.translation import ugettext_lazy as _

CONTEXT_PREFIX = 'unit_'

UNITS = {
    'weight':{
        'verbose_name': _('Weight'),
        'default': 'kg',
        'precision': 2,
        'choices': (
            ('kg', _('Kilogramme')),
            ('lb', _('Pound'))
        )
    },
    
    'hop':{
        'verbose_name': _('Hop'),
        'default': 'g',
        'choices': (
            ('g', _('Gramme')),
            ('oz', _('Ounce'))
        )
    },
    
    'volume':{
        'verbose_name': _('Volume'),
        'default': 'l',
        'precision': 1,
        'choices': (
            ('l', _('Litre')),
            ('gal', _('Gallon'))
        )
    },

    'temperature':{
        'verbose_name': _('Temperature'),
        'default': 'c',
        'choices': (
            ('c', _('deg. C')),
            ('f', _('deg. F'))
        )
    },

    'color':{
        'verbose_name': _('Color'),
        'default': 'ebc',
        'precision': 1,
        'choices': (
            ('ebc', _('EBC')),
            ('srm', _('SRM'))
        )
    },
}
