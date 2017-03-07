from django.test import TestCase
from .forms import *

# NOTE: Run tests using this command: 'python.exe ./manage.py test HNApp.tests'

"""
Below are all of the unit tests for models.py
"""


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

"""
Below are all the unit tests for forms.py
"""


class SignUpFormTest(TestCase):
    """
    Unit tests for SignUpForm
    """
    def setUp(self):
        self.form_data = {'first_name': 'Jane',
                          'last_name': 'Doe',
                          'username': 'JD123',
                          'password': 'password'}

        self.SUF = SignUpForm(data=self.form_data)

    def test_validity(self):
        self.assertTrue(self.SUF.is_valid())


class PatientSignUpTest(TestCase):
    """
    Unit tests for PatientSignUp
    """
    def setUp(self):
        self.form_data = {'dob': '2001-01-01',
                          'contact_info': '123-4567',
                          'emergency_info': 'info',
                          'allergies': 'AllergenA, AllergenB'}

        self.PSU = PatientSignUp(data=self.form_data)

    def test_validity(self):
        self.assertTrue(self.PSU.is_valid())


class CreateMedicalRecordsFormTest(TestCase):
    """
    Unit tests for CreateMedicalRecordsForm.
    NOTE: Gives issues presently
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
                                              emergency_info="info",
                                              allergies="AllergenA, AllergenB",
                                              )

        self.form_data = {'patient': Patient.objects.get(pk=1),
                          'allergies': self.patient.allergies,
                          'current_status': 'Injured',
                          'current_hospital': 'HospitalC',
                          'previous_hospitals': 'HospitalA, HospitalB'}

        self.form = CreateMedicalRecordsForm(data=self.form_data)

    def test_validity(self):
        print(self.form)
        self.assertTrue(self.form.is_valid())

    def tearDown(self):
        self.patient.delete()
        self.u1.delete()


class EditPatientProfileFormTest(TestCase):
    """
    Unit tests for EditPatientProfileForm
    """
    def setUp(self):
        self.form_data = {'dob': '2001-01-01',
                          'contact_info': '123-4567',
                          'emergency_info': 'info',
                          'allergies': 'AllergenA, AllergenB'}

        self.form = EditPatientProfileForm(data=self.form_data)

    def test_validity(self):
        self.assertTrue(self.form.is_valid())


class EditStaffProfileFormTest(TestCase):
    """
    Unit tests for EditStaffProfileForm
    """
    def setUp(self):
        self.form_data = {'first_name': 'Jane',
                          'last_name': 'Doe',
                          'specialization': 'Cardiology',
                          'current_hospital': 'HospitalA'}

        self.form = EditStaffProfileForm(data=self.form_data)

    def test_validity(self):
        self.assertTrue(self.form.is_valid())


class EditMedicalRecordsFormTest(TestCase):
    """
    Unit tests for EditMedicalRecordsForm
    """
    def setUp(self):
        self.form_data = {'allergies': 'Whatever',
                          'current_status': 'Injured',
                          'current_hospital': 'HospitalC',
                          'previous_hospitals': 'HospitalA, HospitalB'}

        self.form = EditMedicalRecordsForm(data=self.form_data)

    def test_validity(self):
        self.assertTrue(self.form.is_valid())
