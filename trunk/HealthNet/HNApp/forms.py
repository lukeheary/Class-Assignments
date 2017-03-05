from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
import sys

from datetime import datetime


"""
This SignUpForm has to be made specifically for the User built-in class
"""
class SignUpForm(ModelForm):
    """
    TODO
    """
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'password')
        exclude = ('email',)

    def save(self, commit=True):
        """
        TODO
        :param commit:
        :return:
        """
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


"""
This is the PatientSignUp extended form from SignUpForm
"""
class PatientSignUp(ModelForm):
    class Meta:
        model = Patient
        fields = ['dob', 'contact_info', 'allergies']

    def save(self, cUser, commit=True):
        """
        TODO
        :param cUser:
        :param commit:
        :return:
        """
        """
        Because 'cUser' is a User class and a foreign key, it has to be saved as attribute 'user'
        """
        user = super(PatientSignUp, self).save(commit=False)
        user.user = cUser
        user.dob = self.cleaned_data['dob']
        user.contact_info = self.cleaned_data['contact_info']
        # user.emergency_info = self.cleaned_data['emergency_info']
        user.allergies = self.cleaned_data['allergies']
        # user.preferred_hospital = self.cleaned_data['preferred_hospital']
        if (commit):
            user.save()
        return user


class ToolForm(ModelForm):
    """
    TODO
    """
    name = forms.CharField()
    birth_date = forms.DateField()
    appointment_list = forms.DateTimeField()

    class Meta:
        model = Patient
        
        fields = ['name', 'birth_date', 'appointment_list']


class AppointmentForm(ModelForm):
    """
    TODO
    """
    class Meta:
        model = Appointment
        datetime = forms.DateTimeField()
        patient = forms.ModelChoiceField(queryset=Patient.objects.all().order_by('name'))
        doctor = forms.ModelChoiceField(queryset=Doctor.objects.all().order_by('name'))
        fields = ['datetime', 'patient', 'doctor']


class EditMedicalRecordsForm(ModelForm):
    """
    TODO
    """
    class Meta:
        model = MedicalRecords
        fields = ['patient', 'current_hospital', 'allergies', 'current_status', 'previous_hospitals']
