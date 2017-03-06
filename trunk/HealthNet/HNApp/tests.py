from django.test import TestCase
from .models import *

# NOTE: Run tests using this command: 'python.exe ./manage.py test HNApp.tests'


class PatientModelTest(TestCase):
    """
    Unit tests for Patient model in models.py
    """
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


class DoctorModelTest(TestCase):
    """
    Unit tests for Doctor model in models.py
    """
    def setUp(self):
        self.u1 = User.objects.create(username="JD123",
                                      password="password",
                                      first_name="Jane",
                                      last_name="Doe"
                                      )

        self.doctor = Doctor.objects.create(user=self.u1,
                                            dob="2001-01-01",
                                            first_name="Dr. Jane",
                                            last_name="Doe",
                                            specialization="Cardiology",
                                            current_hospital="HospitalA",
                                            )

    def test_string_representation(self):
        self.assertEqual(str(self.doctor), "Dr. Jane Doe")

    def tearDown(self):
        self.doctor.delete()
        self.u1.delete()


class NurseModelTest(TestCase):
    """
    Unit tests for Nurse model in models.py
    """
    def setUp(self):
        self.u1 = User.objects.create(username="JD123",
                                      password="password",
                                      first_name="Jane",
                                      last_name="Doe"
                                      )

        self.nurse = Doctor.objects.create(user=self.u1,
                                           dob="2001-01-01",
                                           first_name="Nurse Jane",
                                           last_name="Doe",
                                           specialization="Cardiology",
                                           current_hospital="HospitalA",
                                           )

    def test_string_representation(self):
        self.assertEqual(str(self.nurse), "Nurse Jane Doe")

    def tearDown(self):
        self.nurse.delete()
        self.u1.delete()


class EmergencyContactInfoModelTest(TestCase):
    """
    Unit tests for EmergencyContactInfo model in models.py
    """
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
        self.assertEqual(str(self.EMC), "Jane Doe: John Doe, (111)-222-3333")

    def tearDown(self):
        self.EMC.delete()
        self.patient.delete()
        self.u1.delete()


class AppointmentModelTest(TestCase):
    """
    Unit tests for Appointment model in models.py
    """
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

        self.u2 = User.objects.create(username="AS456",
                                      password="password2",
                                      first_name="Aaron",
                                      last_name="Smith"
                                      )

        self.doctor = Doctor.objects.create(user=self.u2,
                                            dob="2001-01-01",
                                            first_name="Dr. Aaron",
                                            last_name="Smith",
                                            specialization="Cardiology",
                                            current_hospital="HospitalA",
                                            )

        self.appointment = Appointment.objects.create(datetime="2016-12-12 12:00",
                                                      patient=self.patient,
                                                      doctor=self.doctor)

    def test_string_representation(self):
        self.assertEqual(str(self.appointment), "JD123 seeing doctor: Smith at 2016-12-12 12:00")

    def tearDown(self):
        self.appointment.delete()
        self.doctor.delete()
        self.u2.delete()
        self.patient.delete()
        self.u1.delete()


class MedicalRecordModelTest(TestCase):
    """
    Unit tests for MedicalRecord Model in models.py
    """
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

        self.records = MedicalRecord.objects.create(patient=self.patient,
                                                    current_hospital="HospitalA",
                                                    current_status="Healthy",
                                                    previous_hospitals="HospitalB"
                                                    )

    def test_string_representation(self):
        self.assertEqual(str(self.records), "Jane Doe: HospitalA, Healthy")

    def test_set_current_hospital(self):
        self.records.set_current_hospital("HospitalC")
        self.assertEqual(self.records.current_hospital, "HospitalC")
        self.assertEqual(self.records.previous_hospitals, "HospitalA, HospitalB")

    def tearDown(self):
        self.records.delete()
        self.patient.delete()
        self.u1.delete()
