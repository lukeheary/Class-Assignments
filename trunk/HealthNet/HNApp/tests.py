from django.test import TestCase
from .models import *


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
