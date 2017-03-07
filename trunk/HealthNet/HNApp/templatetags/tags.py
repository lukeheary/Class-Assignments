from django import template
from ..models import *
from django.contrib.auth.models import AnonymousUser

register = template.Library()


@register.assignment_tag
def get_user_type(request):
    """
    get_user_type determines if the person viewing the site is a
    patient, doctor, nurse, or isn't logged in
    :param request: the request of the user who is on the site
    :return: a number as a string indicating who is logged in
    """
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


@register.assignment_tag
def get_sys_log(request):
    """
    get_sys_log returns all the lines of the sys.txt in a list
    :param request: the request of the user who is on the site
    :return: list of lines
    """
    all_lines = []
    f = open('sys.txt', 'r')
    for line in f:
        all_lines.append(line)
    return all_lines


@register.assignment_tag
def get_id(request):
    """
    get_id gets the id of the user who is currently logged in
    :param request: the request of the user who is on the site
    :return: users id
    """
    if hasattr(request, 'user'):
        return str(request.user.id)
    else:
        return ''


@register.assignment_tag
def get_num_of_appt(user, all_appointments, request):
    """
    get_id gets the id of the user who is currently logged in
    :param request: the request of the user who is on the site
    :return: users id
    """
    if user == '1' or user == '2':
        return '-1'
    for appointment in all_appointments:
        count = 0
        if appointment.patient.user.id == int(user):
            count += 1
        return count
