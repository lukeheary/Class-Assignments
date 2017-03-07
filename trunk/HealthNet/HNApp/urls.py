from django.conf.urls import url
from . import views

handler404 = 'HNApp.views.handler404'
app_name = 'HNApp'
urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),


    # /accounts...
    # /accounts/patient_signup/
    url(r'^accounts/patient_signup/$', views.register, name="patient_signup"),
    # /accounts/patient_signup/true/
    url(r'^accounts/patient_signup/True/$', views.register, name="register"),
    # /accounts/patient_signup/false
    url(r'^accounts/patient_signup/False/$', views.invalid_login, name="invalid_login"),
    # /accounts/register_success/
    url(r'^accounts/register_success/$', views.register_success, name="register_success"),
    # /accounts/login/
    url(r'^accounts/login/$', views.login, name='login'),
    # /accounts/auth/
    url(r'^accounts/auth/$', views.auth_view, name ='auth_view'),
    # /accounts/logout/
    url(r'^accounts/logout/$', views.logout, name='logout'),
    # /accounts/loggedin/
    url(r'^accounts/loggedin/$', views.loggedin, name='loggedin'),
    # /accounts/invalid_login/
    url(r'^accounts/invalid_login/$', views.invalid_login, name='invalid_login'),
    # /accounts/profile/patient/pkid
    url(r'^accounts/profile/patient/(?P<pk>[0-9]+)/$', views.profile_patient, name='profile_patient'),
    # /accounts/profile/doctor/pkid
    url(r'^accounts/profile/doctor/(?P<pk>[0-9]+)/$', views.profile_doctor, name='profile_doctor'),
    # /accounts/profile/nurse/pkid
    url(r'^accounts/profile/nurse/(?P<pk>[0-9]+)/$', views.profile_nurse, name='profile_nurse'),
    # /accounts/profile/edit_patient_profile/pkid
    url(r'accounts/profile/edit_patient_profile/(?P<pk>[0-9]+)/', views.EditProfileView.as_view(), name='edit_patient_profile'),
    # /accounts/profile/edit_staff_profile/pkid
    url(r'accounts/profile/edit_staff_profile/(?P<pk>[0-9]+)/$', views.EditProfileView.as_view(), name='edit_staff_profile'),


    # appointments...
    # /create-appointment
    url(r'^create_appointment/$', views.CreateAppointmentView.as_view(), name='create_appointment'),
    # time slot is taken
    url(r'^create_appointment/time_taken$', views.time_taken, name='time_taken'),
    # /edit_appointment
    url(r'^edit_appointment/(?P<pk>[0-9]+)/$', views.EditAppointment.as_view(), name='edit_appointment'),
    # /edit_appointment/time_taken
    url(r'^edit_appointment/time_taken/$', views.time_taken, name='time_taken'),


    # lists...
    # /patient-list
    url(r'^patient_list/$', views.patient_list, name='patient_list'),
    # /appointment_list
    url(r'^appointment_list', views.appointment_list, name='appointment_list'),


    # admin...
    # /admin/admin_log
    url(r'^admin/admin_log/$', views.display_log, name='admin_log'),


    # /edit_medical_record
    url(r'accounts/profile/edit_medical_records/(?P<pk>[0-9]+)/$', views.EditMedicalRecordView.as_view(), name='edit_medical_record'),
    #create_medical_record
    url(r'create_medical_records/$', views.CreateMedicalRecordView.as_view(), name='create_medical_record'),
    #accounts/view_medical_record
    url(r'medical_record/(?P<pk>[0-9]+)/$', views.medical_record, name='medical_record'),
    
]
