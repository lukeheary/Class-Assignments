from django.http import HttpResponse
from .forms import *
from django.template import loader, RequestContext
from django.views.generic import View
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
import time
from django.core.urlresolvers import reverse


def index(request):
    """
    Brings up our home page.
    :param request: HTTP Request
    :return: HttpResponse rendered index.html
    """
    all_patients = Patient.objects.all()
    template = loader.get_template('HNApp/index.html')
    context = {
        'all_patients': all_patients
    }
    return HttpResponse(template.render(context, request))


def login(request):
    """
    Brings up our login view.
    :param request: HTTP Request
    :return: HttpResponse rendered login.html
    """
    c = {}
    c.update(csrf(request))
    return render_to_response('HNApp/login.html', c)


# before we have username, pass empty string ''
def auth_view(request):
    """
    Authenticate Registration Information
    :param request: HTTP Request
    :return: HttpResponseRedirect to 'accounts/loggedin' if user is existing
    :return: HttpResponseRedirect to '/accounts/invalid_login' if user is not existing
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        # Later on we can change loggedin to user_homepage, for whatever type of user is it
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid_login')


def loggedin(request):
    """
    Confirm that user is loggedin and redirect them to the homepage
    :param request: HTTP Request
    :return: The rendered 'loggedin.html'
    """
    tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
    str = request.user.username + "signed in." + tm
    print(str)
    return render_to_response('loggedin.html', {'full_name': request.user.username})


def invalid_login(request):
    """
    Inform that the login input is not correct
    :param request: HTTP Request
    :return: The rendered 'invalid_login.html'
    """
    return render_to_response('invalid_login.html')


def display_log(request):
    """
    Display the system log
    :param request: HTTP Request
    :return: HttpResponse rendered 'HNApp/admin_log.html'
    """
    f = open('sys.txt', 'r')
    allStrings = ""
    for line in f:
        allStrings = allStrings + line
    template = loader.get_template('HNApp/admin_log.html')
    context = {
        'allStrings': allStrings
    }
    f = open("sys.txt", 'a')
    sys.stdout = f
    return HttpResponse(template.render(context, request))


def logout(request):
    """
    Log the user out
    :param request: HTTP Request
    :return: Redirect to the homepage
    """
    f = open('sys.txt', 'a')
    sys.stdout = f
    tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
    str = request.user.username + "logged out: " + tm
    print(str)
    auth.logout(request)
    return redirect('/')


def register(request):
    """
    Register Patients 
    :param request: HTTP Request
    :return: If request is a POST, direct user to '/accounts/register_success'
    :return: If request is GET, render 'patient_sigup.html'
    """
    if request.method == 'POST':
        form1 = SignUpForm(data=request.POST)
        form2 = PatientSignUp(data=request.POST)
        if form2.is_valid() and form1.is_valid():
            user = form1.save()
            form2.save(cUser=user)
            f = open('sys.txt', 'a')
            sys.stdout = f
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = user.first_name + "successfully registered: " + tm
            print(str)
            return HttpResponseRedirect('/accounts/register_success')
        else:
            #If input is invalid, render the form again
            return render(request, 'patient_signup.html', 
            {
                'form1':SignUpForm(),
                'form2':PatientSignUp()
            })
    else:
        return render(request, 'patient_signup.html', 
        {
            'form1':SignUpForm(),
            'form2':PatientSignUp()
        })


def register_success(request):
    """
    Confirm that the user has registered successfully.
    :param request: HTTP Request
    :return: If input is valid, direct user to 'register_success.html' page and then immediately lead to the Login page
    :return: If input is invalid, render the signup form again
    """
    return render_to_response('register_success.html')


def profile_patient(request, pk):
    """
    Rendered view_profile.html to help patients view their profile
    :param request: HTTP Request
    :param pk: the id of the Patient object
    :return: HttpResponse rendered 'view_profile.html'
    """
    template = loader.get_template('HNApp/view_profile.html')
    user = Patient.objects.get(pk=pk)
    dob = str(user.dob)
    patient = Patient.objects.all().filter(pk=pk)
    records = MedicalRecord.objects.all().filter(patient=patient)
    if len(records) is not 0:
        record = records[0]
        context = {
            'patient': user,
            'dob': dob,
            'user': '0',
            'record': record,
        }
    else:
        context = {
            'patient': user,
            'dob': dob,
            'user': '0',
        }
    return HttpResponse(template.render(context, request))

def doctor_view_patient(request, pk):
    template = loader.get_template('HNApp/doctor_view_patient.html')
    patient = Patient.objects.get(pk=pk)
    dob = str(patient.dob)
    records = MedicalRecord.objects.all().filter(patient=patient)
    if len(records) is not 0:
        record = records[0]
        context = {
            'patient': patient,
            'dob': dob,
            'record': record,
            'has_record': 'yes'
        }
    else:
        context = {
            'patient': patient,
            'dob': dob,
            'has_record': 'no'
        }
    return HttpResponse(template.render(context, request))



def profile_doctor(request, pk):
    """
    Rendered view_profile.html to help doctors view their profile
    :param request: HTTP Request
    :param pk: the id of the Doctor object
    :return: HttpResponse rendered 'view_profile.html'
    """
    template = loader.get_template('HNApp/view_profile.html')
    user = Doctor.objects.get(pk=pk)
    dob = str(user.dob)
    context = {
        'doctor': user,
        'dob': dob,
        'user': '1',
    }
    return HttpResponse(template.render(context, request))


def profile_nurse(request, pk):
    """
    Rendered view_profile.html to help nurses view their profile
    :param request: HTTP Request
    :param pk: the id of the Nurse object
    :return: HttpResponse rendered 'view_profile.html'
    """
    template = loader.get_template('HNApp/view_profile.html')
    user = Nurse.objects.get(pk=pk)
    dob = str(user.dob)
    context = {
        'nurse': user,
        'dob': dob,
        'user': '2',
    }
    return HttpResponse(template.render(context, request))


def patient_list(request):
    """
    Display the list of patients
    :param request: HTTP Request
    :return: HttpResponse rendered 'patient_list.html'
    """
    all_patients = Patient.objects.all()
    template = loader.get_template('HNApp/patient_list.html')
    context = {
        'all_patients': all_patients
    }
    return HttpResponse(template.render(context, request))


def appointment_list(request):
    """
    Display the list of appointments of each doctor
    :param request: HTTP Request
    :return: HttpResponse rendered 'appointment_list.html'
    """
    all_appointments = Appointment.objects.all()
    template = loader.get_template('HNApp/appointment_list.html')
    context = {
        'all_appointments': all_appointments
    }
    return HttpResponse(template.render(context, request))


class EditProfileView(View):
    """
    Edit profile view
    :param View: Django based view View
    :return: If request is GET, render the form again 
    :return: If request is POST, direct patients to view their profiles
    """
    model = User
    form_class = EditPatientProfileForm
    template_name = 'HNApp/edit_patient_profile.html'

    def get(self, request, pk):
        """
        If request is GET, render the form 'edit_patient_profile.html'
        :param self: The View
        :param request: HTTP Request
        :param pk: The patient's id
        """
        if hasattr(request.user, 'patient'):
            patient = Patient.objects.get(pk=pk)
            form_class = EditPatientProfileForm
            template_name = 'HNApp/edit_patient_profile.html'
            form = self.form_class(initial={
                                        'emergency_info' : patient.emergency_info,
                                        'contact_info': patient.contact_info,
                                        'dob': patient.dob,
                                        'allergies': patient.allergies})
            return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        """
        If request is POST, direct patients to view their profile
        :param self: The View
        :param request: HTTP Request
        :param pk: The patient's id
        :return: Direct patient back to their profile page
        """
        form = self.form_class(request.POST)

        # If the form is valid
        if form.is_valid():
            patient = Patient.objects.get(pk=pk)
            emergency_info = form.cleaned_data['emergency_info']
            contact_info = form.cleaned_data['contact_info']
            dob = form.cleaned_data['dob']
            allergies = form.cleaned_data['allergies']
            patient.emergency_info = emergency_info
            patient.contact_info = contact_info
            patient.dob = dob
            patient.allergies = allergies

            # Later on will work on to let doctors and nurses to edit their profile
            """if meType.equals('Doctor') or meType.equals('Nurse'):
                first_name = form.cleaned_data['first name']
                last_name = form.cleaned_data['last name']
                specialization = form.cleaned_data['specialization']
                current_hospital = form.cleaned_data['current hospital']
                me.first_name = first_name
                me.last_name = last_name
                me.specialization = specialization
                me.current_hospital = current_hospital
            """
            patient.save()
            orig_out = sys.stdout
            f = open('sys.txt', 'a')
            sys.stdout = f
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = request.user.username + " edited their profile: " + tm
            print(str)
            f.close()
            sys.stdout = orig_out
        
        return redirect('/accounts/profile/patient/' + pk)


class EditMedicalRecordView(View):
    """
    Edit medical record view
    :param View: Django based view View
    :return: If request is GET, render the form again 
    :return: If request is POST, direct doctors or nurses to the patient list page
    """
    model = MedicalRecord
    template_name = 'HNApp/edit_medical_records.html'
    form_class = EditMedicalRecordsForm

    def get(self, request, pk):
        
        """
        If request is GET, render the form 'edit_patient_profile.html'
        :param self: The View
        :param request: HTTP Request
        :param pk: The patient's id
        """
        
        patient = Patient.objects.get(pk=pk)
        records = MedicalRecord.objects.all().filter(patient=patient)
       
        form = self.form_class(initial={
                                        'allergies': records[0].allergies,
                                        'current_hospital': records[0].current_hospital,
                                        'previous_hospitals': records[0].previous_hospitals,
                                        'current_status': records[0].current_status})
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        
        """
        If request is GET, render the form 'edit_patient_profile.html'
        :param self: The View
        :param request: HTTP Request
        :param pk: The patient's id
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=pk)
            records = MedicalRecord.objects.all().filter(patient=patient)
            record = records[0]
            allergies = form.cleaned_data['allergies']
            current_status = form.cleaned_data['current_status']
            current_hospital = form.cleaned_data['current_hospital']
            previous_hospitals = form.cleaned_data['previous_hospitals']
            record.allergies = allergies
            record.current_status = current_status
            record.current_hospital = current_hospital
            record.previous_hospitals = previous_hospitals
            record.save()

            orig_out = sys.stdout
            f = open('sys.txt', 'a')
            sys.stdout = f
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = request.user.username + " edited the record of: " + records[0].patient.user.username + tm
            print(str)
            f.close()
            sys.stdout = orig_out
        return redirect('/medical_record/' + pk)


class CreateAppointmentView(View):
    """
    Prompts user for a date, a doctor, and a patient. If the date has already been taken for the selected doctor or
    patient the page gets redirected to 'time_taken.html' and asks you to try again.
    """
    model = Appointment
    form_class = AppointmentForm
    template_name = 'HNApp/create_appointment.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            datetime = form.cleaned_data['datetime']
            patient = form.cleaned_data['patient']
            doctor = form.cleaned_data['doctor']
            all_appointments = Appointment.objects.all()
            for app in all_appointments: # loop through the doctors to see if that time has been taken
                if app.doctor == doctor:
                    if app.datetime == datetime:
                        return HttpResponseRedirect('time_taken')
                if app.patient == patient:
                    if app.datetime == datetime:
                        return HttpResponseRedirect('time_taken')
            appointment.datetime = datetime
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.save()

            if appointment is not None:
                # will redirect to a profile page or a view calender page once that is made
                f = open('sys.txt', 'a')
                sys.stdout = f
                dt = datetime.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
                tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
                str = patient.user.first_name + "made appointment with " + doctor.user.first_name + " at " + dt + ": " + tm
                print(str)
                return redirect('HNApp:appointment_list')

        return render(request, self.template_name, {'form': form})


def medical_record(request, pk):
    """
    TODO
    :param request:
    :return:
    """
    template = 'HNApp/doctor_view_patient.html'

    patient = Patient.objects.get(pk=pk)
    dob = str(patient.dob)
    all_records = MedicalRecord.objects.all()
    records = MedicalRecord.objects.all().filter(patient=patient)
    record = records[0]
    context = {
            'patient': patient,
            'dob': dob,
            'record': record,
            'has_record': 'yes'
    }
    return render( request, template, context)


class CreateMedicalRecordView(View):
    """
    TODO
    """
    model = MedicalRecord
    template_name = 'HNApp/create_medical_records.html'
    form_class = CreateMedicalRecordsForm

    def get(self, request, pk):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            records = form.save(commit=False)

            patient = form.cleaned_data['patient']
            allergies = form.cleaned_data['allergies']
            current_status = form.cleaned_data['current_status']
            current_hospital = form.cleaned_data['current_hospital']
            previous_hospitals = form.cleaned_data['previous_hospitals']

            records.patient = patient
            records.patient.allergies = allergies
            records.current_status = current_status
            records.current_hospital = current_hospital
            records.previous_hospitals = previous_hospitals
            records.save()
            if records is not None:
                orig_out = sys.stdout
                f = open('sys.txt', 'a')
                sys.stdout = f
                tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
                str = request.user.username + " created the medical records for " + patient.user.username + ": " + tm
                print(str)
                f.close()
                sys.stdout = orig_out
                return redirect(reverse('HNApp:medical_record', args=[records.id]))
                
        return render(request, self.template_name, {'form': form})


class EditAppointment(View):
    """
    TODO
    """
    model = Appointment
    form_class = AppointmentForm
    template_name = 'HNApp/edit_appointment.html'

    def get(self, request, pk):
        app = Appointment.objects.get(pk=pk)
        form = self.form_class(None,
                               initial={'datetime': app.datetime, 'patient': app.patient, 'doctor': app.doctor})
        app.delete()
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            datetime = form.cleaned_data['datetime']
            patient = form.cleaned_data['patient']
            doctor = form.cleaned_data['doctor']
            all_appointments = Appointment.objects.all()
            for app in all_appointments:  # loop through the doctors to see if that time has been taken
                if app.doctor == doctor:
                    if app.datetime == datetime:

                        return HttpResponseRedirect('time_taken')
                if app.patient == patient:
                    if app.datetime == datetime:
                        return HttpResponseRedirect('time_taken')
            appointment.datetime = datetime
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.save()

            if appointment is not None:
                # will redirect to a profile page or a view calender page once that is made
                f = open('sys.txt', 'a')
                sys.stdout = f
                dt = datetime.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
                tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
                str = patient.user.username + "made appointment with " + doctor.last_name + " at " + dt + ": " + tm
                print(str)
                return redirect('HNApp:appointment_list')

        return render(request, self.template_name, {'form': form})


def time_taken(request):
    """
    TODO
    :param request:
    :return:
    """
    return render_to_response('time_taken.html')


def handler404(request):
    """
    TODO
    :param request:
    :return:
    """
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response
