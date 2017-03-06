from django import template
from ..models import *
from django.contrib.auth.models import AnonymousUser

register = template.Library()


@register.simple_tag
def active(request, pattern):
    import re
    print(pattern + " : " + request.path)
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.assignment_tag
def get_user_type(request):
    if hasattr(request, 'user'):
        if hasattr(request.user, 'patient'):
            return '0'
        elif hasattr(request.user, 'doctor'):
            return '1'
        elif hasattr(request.user, 'nurse'):
            return '2'
        else:
            return ''
    else:
        return ''
