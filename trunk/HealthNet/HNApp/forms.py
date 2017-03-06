from .models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
import sys


class SignUpForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    """
    Form used for user sign-up.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        exclude = ('email',)

    def save(self, commit=True):
        """
        Saves the information filled out in the form to a new user model in the database.
        :return: the new user
        """
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PatientSignUp(ModelForm):
    """
    Form used for patient sign-up, extends SignUpForm.
    """
    class Meta:
        model = Patient
        fields = ['dob', 'contact_info', 'emergency_info', 'allergies']

    def save(self, cUser, commit=True):
        """
        Saves the information filled out by a new user.
        :param cUser: the current user
        :return: the new user (patient)
        """
        """
        Because 'cUser' is a User class and a foreign key, it has to be saved as attribute 'user'
        """
        user = super(PatientSignUp, self).save(commit=False)
        user.user = cUser
        user.dob = self.cleaned_data['dob']
        user.contact_info = self.cleaned_data['contact_info']
        user.emergency_info = self.cleaned_data['emergency_info']
        user.allergies = self.cleaned_data['allergies']
        # user.preferred_hospital = self.cleaned_data['preferred_hospital']
        if commit:
            user.save()
        return user


class AppointmentForm(ModelForm):
    """
    Form used for filling out appointments, which are associated with a doctor and a patient.
    """
    class Meta:
        model = Appointment
        datetime = forms.DateTimeField()
        patient = forms.ModelChoiceField(queryset=Patient.objects.all().order_by('name'))
        doctor = forms.ModelChoiceField(queryset=Doctor.objects.all().order_by('name'))
        fields = ['datetime', 'patient', 'doctor']


class CreateMedicalRecordsForm(ModelForm):
    """
    Form used for creating medical records, which are associated with a patient.
    """
    class Meta:
        model = MedicalRecord
        patient = forms.ModelChoiceField(queryset=Patient.objects.all().order_by('name'))
        current_status = forms.CharField()
        allergies = forms.CharField()
        current_hospital = forms.CharField()
        previous_hospitals = forms.CharField()
        fields = [ 'patient', 'allergies','current_status','current_hospital',  'previous_hospitals'] 


class EditPatientProfileForm(ModelForm):
    """
    Form used for editing a given patient's profile.
    """
    class Meta:
        model = Patient
        contact_info = forms.CharField()
        emergency_info = forms.CharField()
        dob = forms.DateTimeField()
        allergies = forms.CharField()
        fields = ['contact_info', 'emergency_info', 'dob', 'allergies']


class EditStaffProfileForm(ModelForm):
    """
    Form used for editing a given staff member's profile.
    """
    class Meta:
        model = Doctor
        first_name = forms.CharField()
        last_name = forms.CharField()
        specialization = forms.CharField()
        current_hospital = forms.CharField()
        fields = ['first_name', 'last_name', 'specialization', 'current_hospital']


class EditMedicalRecordsForm(ModelForm):
    """
    Form used for editing a given patient's medical records.
    """
    class Meta:
        model = MedicalRecord
        fields = [ 'allergies','current_hospital', 'current_status', 'previous_hospitals']
