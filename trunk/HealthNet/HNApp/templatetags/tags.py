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

@register.simple_tag
def get_user_type(request):
    user = request.user
    if user == AnonymousUser:
        return "You must first login to view your profile."
    elif user == Patient:
        return "Patient"
    elif user == Doctor:
        return "Doctor"
    elif user == Nurse:
        return "Nurse"
    else:
        return ""
