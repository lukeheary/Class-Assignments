from django.contrib import admin
from .models import *


admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(MedicalRecords)
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


# class PatientAdmin(admin.ModelAdmin):
#     """
#     PatientAdmin defines the layout for registering a patient in the
#     admin console
#     """
#     fieldsets = [
#         ('Basic Information', {'fields': ['name', 'birth_date']}),
#     ]
#     inlines = [EmergencyContactInfoInLine, MedicalRecordsInLine]
#     list_display = ('name', 'birth_date')
#     list_filter = ['name']
#     search_fields = ['name']

# modelsToRegister = [Appointment, Doctor, Nurse]

# admin.site.register(Patient, PatientAdmin)
# admin.site.register(modelsToRegister)
