from django.conf.urls import include, url, handler404
from . import views

handler404 = 'HNApp.views.handler404'
app_name = 'HNApp'
urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),
    # /create
    url(r'^create/$', views.CreateTool.as_view(success_url="/"), name='create'),
    # /accounts/patient_signup/
    url(r'^accounts/patient_signup/$', views.register, name="patient_signup"),
    url(r'^accounts/patient_signup/true$', views.register, name="patient_signup"),
    # Later on can changed by type of users
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
    # /profile
    # url(r'^(?P<name>/profile)/$', views.profile, name=''),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    # /create-appointment
    url(r'^create_appointment/$', views.CreateAppointmentView.as_view(), name='create_appointment'),
    # time slot is taken
    url(r'^create_appointment/time_taken$', views.time_taken, name='time_taken'),
    # /patient-list
    url(r'^patient_list/$', views.patient_list, name='patient_list'),
    # /appointment_list
    url(r'^appointment_list', views.appointment_list, name='appointment_list'),
    # /appointmentid/edit
    #url(r'^(?P<appointment>[0-9]+)/edit', views.EditAppointment, name='edit_appointment')
    url(r'^appointment_list', views.appointment_list, name='appointment_list'),
    # /edit_appointment
    url(r'^edit_appointment/$', views.EditAppointment.as_view(), name='edit_appointment'),
    # /edit_appointment/time_taken
    url(r'^edit_appointment/time_taken', views.time_taken, name='time_taken'),
    # /admin/admin_log
    url(r'^admin/admin_log',views.display_log, name='admin_log'),
    # /edit_medical_record
    url(r'edit_medical_records/(?P<pk>[0-9]+)', views.EditMedicalRecordView.as_view(), name='edit_medical_record'),
    # /create_medical_record
    url(r'create_medical_records', views.CreateMedicalRecordView.as_view(), name='create_medical_record'),
]
