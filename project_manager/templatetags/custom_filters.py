# project_manager/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


# custom_filters.py
from django import template

register = template.Library()

@register.filter
def reverse_order(queryset):
    return reversed(queryset)
