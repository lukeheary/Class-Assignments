from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)


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
    model = MedicalRecord
    fieldsets = [
        (None, {'fields': ['current_hospital', 'current_status', 'allergies']}),
    ]
    max_num = 1



