from django.test import TestCase
from .models import *

# NOTE: Run tests using this command: 'python.exe ./manage.py test HNApp.tests'


class PatientModelTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username="JD123",
                                      password="password",
                                      first_name="Jane",
                                      last_name="Doe"
                                      )

        self.patient = Patient.objects.create(user=self.u1,
                                              dob="2001-01-01",
                                              contact_info="(123)-456-7890",
                                              allergies="AllergenA, AllergenB",
                                              )

    def test_string_representation(self):
        self.assertEqual(str(self.patient), "Jane Doe")

    def tearDown(self):
        self.patient.delete()
        self.u1.delete()


class EmergencyContactInfoModelTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username="JD123",
                                      password="password",
                                      first_name="Jane",
                                      last_name="Doe"
                                      )

        self.patient = Patient.objects.create(user=self.u1,
                                              dob="2001-01-01",
                                              contact_info="(123)-456-7890",
                                              allergies="AllergenA, AllergenB",
                                              )

        self.EMC = EmergencyContactInfo.objects.create(patient=self.patient,
                                                       name="John Doe",
                                                       phone_number="(111)-222-3333")

    def test_string_representation(self):
        self.assertEqual(str(self.EMC), "(Jane Doe: John Doe, (111)-222-3333")

    def tearDown(self):
        self.EMC.delete()
        self.patient.delete()
        self.u1.delete()


class MedicalRecordsModelTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username="JD123",
                                      password="password",
                                      first_name="Jane",
                                      last_name="Doe"
                                      )

        self.patient = Patient.objects.create(user=self.u1,
                                              dob="2001-01-01",
                                              contact_info="(123)-456-7890",
                                              allergies="AllergenA, AllergenB"
                                              )

        self.records = MedicalRecords.objects.create(patient=self.patient,
                                                     current_hospital="Hospital A",
                                                     current_status="Healthy",
                                                     previous_hospitals="Hospital B"
                                                     )

    def test_string_representation(self):
        self.assertEqual(str(self.records), "Jane Doe: HospitalA, Healthy")

    def test_set_current_hospital(self):
        self.records.set_current_hospital(self.records, "HospitalC")
        self.assertEqual(self.records.current_hospital, "HospitalC")
        self.assertEqual(self.records.previous_hospitals, "HospitalB, HospitalA")

    def tearDown(self):
        self.records.delete()
        self.patient.delete()
        self.u1.delete()

