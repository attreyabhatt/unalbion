from django import template

register = template.Library()

@register.filter(name='getattribute')
def getattribute(obj, attr_name):
    try:
        return getattr(obj, attr_name)
    except (AttributeError, TypeError):
        return None

@register.filter
def replace(value, args):
    """Replaces all instances of old with new in the given string"""
    old, new = args.split(',')
    return value.replace(old, new)

@register.filter
def replace_underscore_with_space(value):
    return value.replace('_', ' ')

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def floatval_class(value):
    try:
        val = float(value)
        if val > 0:
            return "success"
        elif val < 0:
            return "danger"
        else:
            return "secondary"
    except:
        return "secondary"

@register.filter
def split(value, delimiter="_"):
    return value.split(delimiter)
