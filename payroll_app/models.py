from django.db import models
from datetime import datetime

class Employee(models.Model):
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    address = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250, null=True)
    mobile = models.CharField(max_length=250, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    salary_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.firstname + ' - ' + self.lastname

class Settings(models.Model):
    hours_per_day = models.IntegerField(default=8)

    def __str__(self):
        return str(self.hours_per_day)

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    punch_in_time = models.TimeField(null=True)
    punch_in_notes = models.CharField(max_length=250, null=True)
    punch_out_time = models.TimeField(null=True)
    punch_out_notes = models.CharField(max_length=250, null=True)
    hours = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.employee.firstname) + ' ' + str(self.employee.lastname) + ' - ' + str(datetime.strftime(self.date, '%d/%m/%Y')) + ' - ' + str(self.punch_in_time) + ' - ' + str(self.punch_out_time) + ' - ' + str(self.hours)

class AdvancePayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.employee.firstname) + ' ' + str(self.employee.lastname) + ' - ' + str(datetime.strftime(self.date, '%d/%m/%Y')) + ' - ' + str(self.amount)


