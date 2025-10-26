from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split_by_comma(value):
    """
    Splits a string by commas.
    """
    return [item.strip() for item in value.split(',') if item.strip()]