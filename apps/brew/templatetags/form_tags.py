# -*- coding: utf-8 -*-
from django.template import Library
from django.conf import settings
from django.template.loader import render_to_string

register = Library()


COLUMN_SIZES = {
    "S": [2, 10],
    "M": [3, 9],
    "L": [4, 8],
    "XL": [5, 7]
}


@register.simple_tag(takes_context=False)
def addFormField(field, label=None, added_css_class="", error_field=None, simple=False,
                 show_help_text=True, size="M", template_name=None):
    """
        Size can be "M" or "L", it plays with the "<label>" column size.
    """
    # Pass this to the context in case you want to extend it
    # and if we want to change the tempalte name later, it will be easier
    base_template_name = "misc/form_field.html"

    if not template_name:
        if simple:
            template_name = "misc/form_field_simple.html"
        else:
            template_name = "misc/form_field.html"
    return render_to_string(
        template_name,
        {
            'base_template_name': base_template_name,
            'field': field,
            'label': label,
            'added_css_class': added_css_class,
            'error_field': error_field,
            'MEDIA_URL': settings.MEDIA_URL,
            'show_help_text': show_help_text,
            'size': COLUMN_SIZES.get(size)
        }
    )


@register.inclusion_tag('misc/form_field_verical.html')
def addFormFieldVerticalForm(field, label=None, added_css_class="", error_field=None, show_help_text=True):
    """
    """
    return {'field': field, 'label': label, 'added_css_class': added_css_class, 'error_field': error_field, 'MEDIA_URL': settings.MEDIA_URL, 'show_help_text': show_help_text}


@register.inclusion_tag('misc/form_field.html')
def addFormFieldWithToolTip(field, tooltip_text, label=None, added_css_class="", error_field=None):
    """
        NOTE: Must keep the order of the parameters, since we the named parameters are not supported in the
        template tag (django 1.3) so when we use them in the templates we put them in the right order
    """
    return {'field': field, 'tooltip_text': tooltip_text, 'label': label, 'added_css_class': added_css_class, 'error_field': error_field}
