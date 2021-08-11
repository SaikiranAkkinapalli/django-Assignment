from django import template

import re

register = template.Library()

@register.filter(name='dict')
def dict(value):
    value=value.replace('{','')
    value=value.replace('}','')
    value=value.replace("'",'')
    #value=eval(value)
    return value