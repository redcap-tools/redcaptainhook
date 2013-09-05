from django import template

register = template.Library()

@register.filter(name="active")
def active_class(value):
    return "" if value else "warning"

