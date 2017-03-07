from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    """
    Holds personal information related to a Patient user.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    dob = models.DateField('Date of Birth', null=True, blank=True, default="")
    contact_info = models.CharField(max_length=10, default="")
    emergency_info = models.CharField(max_length=10, default="")
    allergies = models.CharField(max_length=50, default="")
    user_type = 'Patient'

    def __str__(self):
        """
        __str__ defines the to string method for EmergencyContactInfo
        :return: string - "(Patient's name) Contact's Name, Contact's Number"
        """
        return self.user.first_name + " " + self.user.last_name


class EmergencyContactInfo(models.Model):
    """
    EmergencyContactInfo contains two fields, names and phone_number, that hold
    the necessary information to get in contact with a patient's emergency contact.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=100, default="")
    # Problem for the future: changing the names and phone_numbers of the contacts

    def __str__(self):
        """
        __str__ defines the to string method for EmergencyContactInfo
        :return: string - "Patient's name: Contact's Name, Contact's Number"
        """
        return self.patient.user.first_name + " " + self.patient.user.last_name \
            + ": " + self.name + ", " + self.phone_number


class Doctor(models.Model):
    """
    Holds personal information related to a Doctor user.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    dob = models.DateField('Date of Birth', null=True, blank=True, default="")
    specialization = models.CharField(max_length=50, default="")
    current_hospital = models.CharField(max_length=50, default="")
    user_type = "Doctor"

    def __str__(self):
        """
        __str__ defines the to string method for Doctor
        :return: string - Doctor's name
        """
        name = self.first_name + " " + self.last_name
        return name


class Nurse(models.Model):
    """
    Holds personal information related to a Nurse user.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    dob = models.DateField('Date of Birth', null=True, blank=True, default="")
    specialization = models.CharField(max_length=50, default="")
    current_hospital = models.CharField(max_length=50, default="")
    user_type = "Nurse"
    
    def __str__(self):
        """
        __str__ defines the to string method for Doctor
        :return: string - Nurse's name
        """
        name = self.first_name + " " + self.last_name
        return name 


class Appointment(models.Model):
    """
    Appointment TODO
    """
    # 2006-10-25 14:30
    datetime = models.DateTimeField('appointment time', null=True, blank=True, default='')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default="")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default="")

    def __str__(self):
        """
        __str__ defines the to string method for Appointment
        :return: string - "Patient's Name seeing: Doctor's Name at Date"
        """
        return self.patient.user.username + " seeing doctor: " + self.doctor.last_name + \
            " at " + self.datetime.__str__()


class MedicalRecord(models.Model):
    """
    MedicalRecords holds information pertinent to the user's medical history.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default="")
    allergies = models.CharField(max_length=50, default="") 
    current_status = models.CharField(max_length=50, default="")
    current_hospital = models.CharField(max_length=100, default="")
    previous_hospitals = models.CharField(max_length=200, default="")

    def __str__(self):
        """
        __str__ defines the to string method for MedicalRecords
        :return: string - "Patient's name: Current Hospital, Current Status"
        """
        return self.patient.user.first_name + " " + self.patient.user.last_name + ": " + self.current_hospital \
            + ", " + self.current_status

    def set_current_hospital(self, new_hospital):
        """
        setCurrentHospital sets a patient's current hospital and adds the
        previous current hospital to the previous_hospital list
        :param new_hospital: the new hospital the patient is at
        """
        self.previous_hospitals = self.current_hospital + ", " + self.previous_hospitals
        self.current_hospital = new_hospital


class Admin(models.Model):
    """
    May be implemented in the future
    """
    pass
