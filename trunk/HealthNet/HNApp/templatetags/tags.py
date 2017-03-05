from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    import re
    print(pattern + " : " + request.path)
    if re.search(pattern, request.path):
        return 'active'
    return ''
