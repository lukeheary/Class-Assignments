from django.http import HttpResponse
from .forms import *
from django.template import loader, RequestContext
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
# control user log in/out
from django.contrib import auth
# security purpose
from django.core.context_processors import csrf
import time
from django.core.urlresolvers import reverse


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
    TODO
    :param request:
    :return:
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
            f = open('sys.txt', 'a')
            sys.stdout = f
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = user.first_name + "successfully registered: " + tm
            print(str)
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


def profile(request, pk):
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
    elif hasattr(request.user, 'doctor'):
        working_user = request.user.doctor
        dob = str(request.user.doctor.dob)
        context = {
            'doctor': working_user,
            'dob': dob,
            'user': '1',
        }
        return HttpResponse(template.render(context, request))
    elif hasattr(request.user, 'nurse'):
        working_user = request.user.nurse
        dob = str(request.user.nurse.dob)
        context = {
            'nurse': working_user,
            'dob': dob,
            'user': '2',
        }
        return HttpResponse(template.render(context, request))
    else:
        context = {
            'user': '3'
        }
        return HttpResponse(template.render(context, request))


def patient_list(request):
    """
    TODO
    :param request: HTTP Request
    :return: HttpResponse
    """
    all_patients = Patient.objects.all()
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


class LoginTool(View):
    """
    TODO
    """
    model = User
    form_class = SignUpForm
    template_name = 'HNApp/login.html'


class EditProfileView(View):
    """
    TODO
    """
    model = User
    form_class = EditPatientProfileForm
    template_name = 'HNApp/edit_patient_profile.html'

    def get(self, request, pk):
        if hasattr(request.user, 'patient'):
            patient = Patient.objects.get(pk=pk)
            form_class = EditPatientProfileForm
            template_name = 'HNApp/edit_patient_profile.html'
            form = self.form_class(initial={
                                        #'first name': patient.user.username,
                                        #'last name': patient.user.last_name,
                                        'emergency_info' : patient.emergency_info,
                                        'contact_info': patient.contact_info,
                                        'dob': patient.dob,
                                        'allergies': patient.allergies})
            return render(request, self.template_name, {'form': form})
        if hasattr(request.user, 'doctor') or hasattr(request.user, 'nurse'):

            form = self.form_class(initial={'first name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'specialization': request.user.specialization,
                                            'current hospital': request.user.current_hospital})
            return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=pk)
            #first_name = form.cleaned_data['patient.user.username']
            #last_name = form.cleaned_data['user.last_name']
            contact_info = form.cleaned_data['contact_info']
            dob = form.cleaned_data['dob']
            allergies = form.cleaned_data['allergies']
            #patient.user.username = first_name
            #patient.user.last_name = last_name
            patient.contact_info = contact_info
            patient.dob = dob
            patient.allergies = allergies

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

        return redirect('/accounts/profile/' + pk)


class EditMedicalRecordView(View):
    """
    TODO
    """
    model = MedicalRecord
    template_name = 'HNApp/edit_medical_records.html'
    form_class = EditMedicalRecordsForm

    def get(self, request, pk):
        records = MedicalRecord.objects.get(pk=pk)
        form = self.form_class(initial={
                                        'allergies': records.allergies,
                                        'current_hospital': records.current_hospital,
                                        'previous_hospitals': records.previous_hospitals,
                                        'current_status': records.current_status})
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            records = MedicalRecord.objects.get(pk=pk)

            allergies = form.cleaned_data['allergies']
            current_status = form.cleaned_data['current_status']
            current_hospital = form.cleaned_data['current_hospital']
            previous_hospitals = form.cleaned_data['previous_hospitals']

           
            records.allergies = allergies
            records.current_status = current_status
            records.current_hospital = current_hospital
            records.previous_hospitals = previous_hospitals

           

            records.save()

            orig_out = sys.stdout
            f = open('sys.txt', 'a')
            sys.stdout = f
            tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            str = request.user.username + " edited the record of: " + records.patient.user.username + tm
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
    template = 'HNApp/view_medical_record.html'
    record = get_object_or_404(MedicalRecord, pk = pk)
    return render( request, template, {'record':record})


class CreateMedicalRecordView(View):
    """
    TODO
    """
    model = MedicalRecord
    template_name = 'HNApp/create_medical_records.html'
    form_class = CreateMedicalRecordsForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            records = form.save(commit=False)

            patient = form.cleaned_data['patient']
            allergies = form.cleaned_data['allergies']
            current_status = form.cleaned_data['current_status']
            current_hospital = form.cleaned_data['current_hospital']
            previous_hospitals = form.cleaned_data['previous_hospitals']

            records.patient = patient
            records.allergies = allergies
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
        app = Appointment.object.get(pk=pk)
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
                str = patient.user.name + "made appointment with " + doctor.last_name + " at " + dt + ": " + tm
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
