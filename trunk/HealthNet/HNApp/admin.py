from django.contrib import admin
from .models import *


class EmergencyContactInfoInLine(admin.TabularInline):
    """
    TODO
    """
    model = EmergencyContactInfo
    extra = 1


class MedicalRecordsInLine(admin.StackedInline):
    """
    TODO
    """
    model = MedicalRecords
    fieldsets = [
        (None, {'fields': ['current_hospital', 'current_status', 'allergies']}),
    ]
    max_num = 1

modelsToRegister = [Patient, Doctor, Nurse, Appointment]
admin.site.register(modelsToRegister)