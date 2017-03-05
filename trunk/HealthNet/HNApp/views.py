from django.http import HttpResponse
from .models import *
from .forms import *
from django.template import loader, RequestContext
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
# control user log in/out
from django.contrib import auth
# security purpose
from django.core.context_processors import csrf
from django.contrib.auth.models import AnonymousUser
f = open('sys.txt', 'w')
sys.stdout = f
import time
from django.contrib.auth.decorators import login_required


def index(request):
    """
    TODO
    :param request: HTTP Request
    :return: HttpResponse
    """
    all_patients = Patient.objects.all()
    template = loader.get_template('HNApp/index.html')
    context = {
        'all_patients': all_patients
    }
    return HttpResponse(template.render(context, request))


def login(request):
    """
    TODO
    :param request:
    :return:
    """
    c = {}
    c.update(csrf(request))
    return render_to_response('HNApp/login.html', c)


# before we have username, pass empty string ''
def auth_view(request):
    """
    TODO
    :param request:
    :return:
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    print("b")
    if user is not None:
        print("c")
        auth.login(request, user)
        # Later on we can change loggedin to user_homepage, for whatever type of user is it
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        print("d")
        return HttpResponseRedirect('/accounts/invalid_login')


# def user_profile(request):
#     """
#     TODO
#     :param request:
#     :return:
#     """
#     if (request.method == 'POST') :
#         form = UserProfileForm(request.POST, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/accounts/loggedin')
#     else:
#         user = request.user
#         profile = user.profile
#         form = UserProfileForm(instance=profile)
#     args = {}
#     args.update(csrf(request))
#     args['form']=form

#     return render_to_response('doctor_profile.html',args)


def get_user_type(request):
    if hasattr(request.user, 'patient'):
        return 'patient'
    elif hasattr(request.user, 'doctor'):
        return 'doctor'
    elif hasattr(request.user, 'nurse'):
        return 'nurse'
    else:
        return ''


def loggedin(request):
    """
    TODO
    :param request:
    :return:
    """
    tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
    str = request.user.username + "signed in." + tm
    print(str)
    return render_to_response('loggedin.html', {'full_name': request.user.username})


def invalid_login(request):
    """

    :param request:
    :return:
    """
    return render_to_response('invalid_login.html')


def display_log(request):
    f = open('sys.txt', 'r')
    allStrings = ""
    for line in f:
        allStrings = allStrings + line + "\n"

    template = loader.get_template('HNApp/admin_log.html')
    context = {
        'allStrings': allStrings
    }
    f.close()
    f = open("sys.txt",'w')
    sys.stdout = f
    return HttpResponse(template.render(context, request))


def logout(request):
    """
    TODO
    :param request:
    :return:
    """
    auth.logout(request)
    tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
    str = request.user.name + "logged out: " + tm
    print(str)
    return render_to_response('logout.html')


def register(request):
    """
    TODO
    :param request:
    :return:
    """
    if request.method == 'POST':
        form1 = SignUpForm(data=request.POST)
        form2 = PatientSignUp(data=request.POST)
      
        if form2.is_valid() and form1.is_valid():
            user = form1.save()
            form2.save(cUser=user)
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = user.first_name + "successfully registered: " + tm
            return HttpResponseRedirect('/accounts/register_success')
        else:
            
            return HttpResponseRedirect(form2.is_valid())  
    else:
        return render(request, 'patient_signup.html', 
        {
            'form1':SignUpForm(),
            'form2':PatientSignUp()
        })


def register_success(request):
    """
    TODO
    :param request:
    :return:
    """
    return render_to_response('register_success.html')




def profile(request):
    """
    TODO
    :param request:
    :return:
    """
    template = loader.get_template('HNApp/view_profile.html')
    if hasattr(request.user, 'patient'):
        working_user = request.user.patient
        dob = str(request.user.patient.dob)
        context = {
            'patient': working_user,
            'dob': dob,
            'user': '0',
        }
        return HttpResponse(template.render(context, request))
    if hasattr(request.user, 'doctor'):
        working_user = request.user.doctor
        dob = str(request.user.doctor.dob)
        context = {
            'doctor': working_user,
            'dob': dob,
            'user': '1',
        }
        return HttpResponse(template.render(context, request))
    if hasattr(request.user, 'nurse'):
        working_user = request.user.nurse
        dob = str(request.user.nurse.dob)
        context = {
            'nurse': working_user,
            'dob': dob,
            'user': '2',
        }
        return HttpResponse(template.render(context, request))


def patient_list(request):
    """
    TODO
    :param request: HTTP Request
    :return: HttpResponse
    """
    all_patients = User.objects.all()
    template = loader.get_template('HNApp/patient_list.html')
    context = {
        'all_patients': all_patients
    }
    return HttpResponse(template.render(context, request))


def appointment_list(request):
    """
    TODO
    :param request: HTTP Request
    :return: HttpResponse
    """
    all_appointments = Appointment.objects.all()
    template = loader.get_template('HNApp/appointment_list.html')
    context = {
        'all_appointments': all_appointments
    }
    return HttpResponse(template.render(context, request))


class CreateMedicalRecordView(View):
    """
    TODO
    """
    model = MedicalRecords
    template_name = 'HNApp/create_medical_records.html'
    form_class = EditMedicalRecordsForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            records = form.save(commit=False)
            patient = form.cleaned_data['patient']
            current_hospital = form.cleaned_data['current_hospital']
            allergies = form.cleaned_data['allergies']
            current_status = form.cleaned_data['current_status']
            previous_hospitals = form.cleaned_data['previous_hospitals']
            records.patient = patient
            records.current_hospital = current_hospital
            records.allergies = allergies
            records.current_status = current_status
            records.previous_hospitals = previous_hospitals
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = request.user.name + " created the records for " + patient.name + ": " + tm
            print(str)
            records.save()

        return render(request, self.template_name, {'form': form})


class EditMedicalRecordView(View):
    """
    TODO
    """
    model = MedicalRecords
    template_name = 'HNApp/edit_medical_records.html'
    form_class = EditMedicalRecordsForm

    def get(self, request, pk):
        records = MedicalRecords.objects.get(pk=pk)
        form = self.form_class(initial={'patient': records.patient,
                                        'allergies': records.allergies,
                                        'current_hospital': records.current_hospital,
                                        'previous_hospitals': records.previous_hospitals,
                                        'current_status': records.current_status})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            records = form.save(commit=False)
            patient = form.cleaned_data['patient']
            current_hospital = form.cleaned_data['current_hospital']
            allergies = form.cleaned_data['allergies']
            current_status = form.cleaned_data['current_status']
            previous_hospitals = form.cleaned_data['previous_hospitals']
            records.patient = patient
            records.current_hospital = current_hospital
            records.allergies = allergies
            records.current_status = current_status
            records.previous_hospitals = previous_hospitals
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = request.user.name + " edited the records of " + patient.name + ": " + tm
            print(str)
            records.save()

        return render(request, self.template_name, {'form': form})


class CreateTool(CreateView):
    """
    TODO
    """
    model = Patient
    template_name = 'HNApp/tool_form.html'
    form_class = ToolForm


class LoginTool(View):
    """
    TODO
    """
    model = User
    form_class = SignUpForm
    template_name = 'HNApp/login.html'


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
                tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
                str = patient.name + "made appointment with " + doctor.name + " at " + datetime + ": " + tm
                print(str)
                return redirect('HNApp:appointment_list')

        return render(request, self.template_name, {'form': form})


class EditAppointment(View):
    """
    TODO
    """
    model = Appointment
    form_class = AppointmentForm
    template_name = 'HNApp/edit_appointment.html'

    def get(self, request):
        apps = Appointment.objects.all()
        old = apps[0]
        form = self.form_class(None,
                               initial={'datetime': old.datetime, 'patient': old.patient, 'doctor': old.doctor})
        old.delete()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
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
                tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
                str = patient.name + "made appointment with " + doctor.name + " at " + datetime + ": " + tm
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
