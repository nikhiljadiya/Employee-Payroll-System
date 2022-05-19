from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from payroll_app import views as v

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', v.index),
    url(r'^login/$', login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', logout, {'next_page': '/login/'}),
    url(r'^forgot_password/$', v.forgot_password, name='forgot_password'),
    url(r'^reset_password/$', v.reset_password, name='reset_password'),
    url(r'^settings/$', v.settings, name='settings'),
    url(r'^employee/$', v.employee, name='employee'),
    url(r'^employee/(?P<action>\w+)/(?P<employee_id>[0-9]+)/$', v.employee, name='employee_action'),
    url(r'^attendance/$', v.attendance, name='attendance'),
    url(r'^attendance/(?P<action>\w+)/(?P<attendance_id>[0-9]+)/$', v.attendance, name='attendance_action'),
    url(r'^advance_payment/$', v.advance_payment, name='advance_payment'),
    url(r'^advance_payment/(?P<action>\w+)/(?P<advance_payment_id>[0-9]+)/$', v.advance_payment, name='advance_payment_action'),
    url(r'^ajax_employee_last_attendance/$', v.ajax_employee_last_attendance, name='ajax_employee_last_attendance'),
    url(r'^attendance_report/$', v.attendance_report, name='attendance_report'),
    url(r'^salary_report/$', v.salary_report, name='salary_report'),
    url(r'^test_template$', v.test_template),
]
