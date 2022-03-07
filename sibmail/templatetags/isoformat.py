from django import template

register = template.Library()

@register.filter()
def iso_datetime(value):
    from datetime import datetime
    iso = datetime.fromisoformat(value)
    return iso