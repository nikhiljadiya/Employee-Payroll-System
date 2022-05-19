from django.contrib import admin
from .models import Employee, Settings, Attendance, AdvancePayment

admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Settings)
admin.site.register(AdvancePayment)