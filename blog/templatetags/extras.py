from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()

@register.filter()
@stringfilter
def overview(value):
    return value.split('<span id="readmore-anchor" />')[0]
