from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
    value = value.replace('[[readmore_anchor]]', '')
    return md.markdown(value, 
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'pymdownx.arithmatex',
        ],

        extension_configs={
            'pymdownx.arithmatex': {
                'generic': True
                }
        })
@register.filter()
@stringfilter
def overview(value):
    return value.split('[[readmore_anchor]]')[0]
