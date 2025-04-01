from django import template

register = template.Library()

@register.filter
def get_range(value):
    """
    Returns a range of numbers from 0 to value-1
    """
    return range(value) 