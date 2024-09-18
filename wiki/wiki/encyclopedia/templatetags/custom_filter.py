
from django import template

register = template.Library()

@register.filter
def split_extention(value):
    return value.split('.')