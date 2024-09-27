from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(1, value + 1)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''