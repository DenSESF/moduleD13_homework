from django import template


register = template.Library()


@register.filter(name='is_staff')
def is_staff(value):
    return value.groups.filter(name='staff').exists()
