from django.http import Http404, JsonResponse
from django.shortcuts import render, render_to_response, HttpResponse, redirect, get_object_or_404
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Employee, Settings, Attendance, AdvancePayment


def index(request):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    employees = Employee.objects.all().count()
    context['total_employees'] = employees
    return render(request, 'index.html', context)


def settings(request):
    if request.user.is_authenticated() == False:
        return redirect('login')

    if request.method == 'POST':
        settings = Settings.objects.get(pk=1)
        settings.hours_per_day = request.POST['txtHours']
        settings.save()

    settings = Settings.objects.get(pk=1)
    context = {'settings': settings}
    return render(request, 'settings.html', context)


def employee(request, action=None, employee_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    # request.session['message'] = None

    if action == "view":
        employee = get_object_or_404(Employee, pk=employee_id)
        context['employee'] = employee
        context['readonly'] = 1

    elif action == "edit":
        employee = get_object_or_404(Employee, pk=employee_id)
        context['employee'] = employee

    elif action == "delete":
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('employee')

    if request.method == 'POST':
        if employee_id != "" and action == "edit":
            employee = Employee.objects.get(pk=employee_id)
            request.session['message'] = 'Record update successfully.'
        else:
            employee = Employee()
            request.session['message'] = 'Record save successfully.'

        employee.firstname = request.POST['txtFirstname']
        employee.lastname = request.POST['txtLastname']
        employee.address = request.POST['txtAddress']
        employee.phone = request.POST['txtPhone']
        employee.mobile = request.POST['txtMobile']
        employee.salary_per_day = Decimal(request.POST['txtSalary'])
        if request.POST['cmbBalanceType'] == "cr":
            employee.balance = Decimal(request.POST['txtBalance']) * -1
        elif request.POST['cmbBalanceType'] == "dr":
            employee.balance = Decimal(request.POST['txtBalance'])

        employee.save()
        return redirect('employee')

    employees = Employee.objects.all()
    context['all_employees'] = employees
    return render(request, 'employee.html', context)


def attendance(request, action=None, attendance_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    request.session['message'] = None
    employees = Employee.objects.all()
    context['employees'] = employees

    if action == "view":
        attendance = get_object_or_404(Attendance, pk=attendance_id)
        context['attendance'] = attendance
        context['readonly'] = 1

    elif action == "edit":
        attendance = get_object_or_404(Attendance, pk=attendance_id)
        context['attendance'] = attendance

    elif action == "delete":
        attendance = get_object_or_404(Attendance, pk=attendance_id)
        attendance.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('attendance')

    if request.method == 'POST':
        if attendance_id != "" and action == "edit":
            attendance = Attendance.objects.get(pk=attendance_id)
            request.session['message'] = 'Record update successfully.'
        else:
            if request.POST['hfAttendanceId'] != '':
                attendance = Attendance.objects.get(pk=request.POST['hfAttendanceId'])
                attendance.punch_out_time = request.POST['txtTime']
                attendance.punch_out_notes = request.POST['txtNotes']
                time1 = datetime.strptime(str(attendance.punch_in_time), '%H:%M:%S')
                time2 = datetime.strptime(str(attendance.punch_out_time) + ":00", '%H:%M:%S')
                difference = time2 - time1
                m, s = divmod(difference.seconds, 60)
                h, m = divmod(m, 60)
                m = m / 100
                h = h + m
                attendance.hours = Decimal(h)
            else:
                attendance = Attendance()
                attendance.employee = Employee.objects.get(pk=request.POST['cmbEmployee'])
                date = datetime.strptime(str.strip(request.POST['txtDate']), '%d/%m/%Y')
                attendance.date = date.strftime('%Y-%m-%d')
                attendance.punch_in_time = request.POST['txtTime']
                attendance.punch_in_notes = request.POST['txtNotes']

        request.session['message'] = 'Record save successfully.'
        attendance.save()
        return redirect('attendance')

    attendances = Attendance.objects.all()
    context['all_attendance'] = attendances

    return render(request, 'attendance.html', context)


def ajax_employee_last_attendance(request):
    employee_id = request.POST['employee'];
    if Attendance.objects.filter(employee=employee_id).exists():
        last_record = Attendance.objects.filter(employee=employee_id).order_by('-id')[0]
        if last_record.punch_out_time is None:
            context = {'id': last_record.id, 'last_punch_in_time': last_record.punch_in_time, 'last_punch_out_time': '', 'button': 'Punch Out'}
        else:
            context = {'id': '', 'last_punch_in_time': '', 'last_punch_out_time': last_record.punch_out_time, 'button': 'Punch In'}
    else:
        context = {'id': '', 'last_punch_in_time': '', 'last_punch_out_time': '', 'button': 'Punch In'}

    return JsonResponse(context)


def attendance_report(request):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    settings = Settings.objects.get(pk=1)

    if request.method == 'POST':
        date = request.POST['txtDate']
        date_full = date.split('-')
        date1 = datetime.strptime(str.strip(date_full[0]), '%d/%m/%Y')
        date1_main = date1.strftime('%Y-%m-%d')
        date2 = datetime.strptime(str.strip(date_full[1]), '%d/%m/%Y')
        date2_main = date2.strftime('%Y-%m-%d')
        attendances = Attendance.objects.filter(employee=request.POST['cmbEmployee']).filter(date__range=[date1_main, date2_main])

        context['all_attendance'] = attendances
        settings = Settings.objects.get(pk=1)
        context['settings'] = settings

    employees = Employee.objects.all()
    context['employees'] = employees
    context['from_date'] = datetime(datetime.now().year, datetime.now().month, 1)

    return render(request, 'attendance_report.html', context)


def salary_report(request):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    settings = Settings.objects.get(pk=1)

    if request.method == 'POST':
        date = request.POST['txtDate']
        date_full = date.split('-')
        date1 = datetime.strptime(str.strip(date_full[0]), '%d/%m/%Y')
        date1_main = date1.strftime('%Y-%m-%d')
        date2 = datetime.strptime(str.strip(date_full[1]), '%d/%m/%Y')
        date2_main = date2.strftime('%Y-%m-%d')
        attendances = Attendance.objects.filter(employee=request.POST['cmbEmployee']).filter(date__range=[date1_main, date2_main])

        total = 0
        total_hours = 0
        for attendance in attendances:
            total_hours += attendance.hours
            total += Decimal(attendance.hours * attendance.employee.salary_per_day) / settings.hours_per_day

        context['total_salary'] = total
        context['total_hours'] = total_hours

    employees = Employee.objects.all()
    context['employees'] = employees
    context['from_date'] = datetime(datetime.now().year, datetime.now().month, 1)

    return render(request, 'salary_report.html', context)


def advance_payment(request, action=None, advance_payment_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    request.session['message'] = None
    employees = Employee.objects.all()
    context['employees'] = employees

    if action == "view":
        advance_payment = get_object_or_404(AdvancePayment, pk=advance_payment_id)
        context['advance_payment'] = advance_payment
        context['readonly'] = 1

    elif action == "edit":
        advance_payment = get_object_or_404(AdvancePayment, pk=advance_payment_id)
        context['advance_payment'] = advance_payment

    elif action == "delete":
        advance_payment = get_object_or_404(AdvancePayment, pk=advance_payment_id)
        employee = Employee.objects.get(pk=advance_payment.employee.id)
        employee.balance = employee.balance - Decimal(advance_payment.amount)
        employee.save()
        advance_payment.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('advance_payment')

    if request.method == 'POST':
        if advance_payment_id != "" and action == "edit":
            advance_payment = AdvancePayment.objects.get(pk=advance_payment_id)
            employee = Employee.objects.get(pk=advance_payment.employee.id)
            employee.balance = employee.balance - Decimal(advance_payment.amount)
            employee.save()
            request.session['message'] = 'Record update successfully.'
        else:
            advance_payment = AdvancePayment()
            request.session['message'] = 'Record save successfully.'

        employee = Employee.objects.get(pk=request.POST['cmbEmployee'])
        advance_payment.employee = employee
        date = datetime.strptime(str.strip(request.POST['txtDate']), '%d/%m/%Y')
        advance_payment.date = date.strftime('%Y-%m-%d')
        advance_payment.notes = request.POST['txtNotes']
        if request.POST['cmbAmountType'] == "cr":
            employee.balance = employee.balance + (Decimal(request.POST['txtAmount']) * -1)
        elif request.POST['cmbAmountType'] == "dr":
            employee.balance = employee.balance + Decimal(request.POST['txtAmount'])
        employee.save()
        if request.POST['cmbAmountType'] == "cr":
            advance_payment.amount = Decimal(request.POST['txtAmount']) * -1
        elif request.POST['cmbAmountType'] == "dr":
            advance_payment.amount = Decimal(request.POST['txtAmount'])

        advance_payment.save()
        return redirect('advance_payment')

    advance_payments = AdvancePayment.objects.all()
    context['all_advance_payments'] = advance_payments
    return render(request, 'advance_payment.html', context)


def forgot_password(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['txtUsername']
        email = request.POST['txtEmail']
        to_email = "jadiyan@gmail.com"

        user_count = User.objects.filter(username=username).filter(email=email).count()
        if user_count > 0:
            url = request.META['HTTP_HOST'] + '/reset_password'
            ctx = {'user': username, 'page_url' : url}
            html_content = get_template('email.html').render(ctx)

            subject, from_email = 'Employee Payroll System :: Forgot Password', 'nikhil.j@infowaysmedia.com'
            # html_content = '<p>Hi User,</p><p>Your password is : <strong>admin@12345</strong></p><p>Employee Payroll System Team</p>'
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            context['message'] = 'Email send successfully.'
            # context['message'] = html_content
        else:
            context['message'] = 'Enter correct username or email.'

    # send_mail('Test Email', 'Here is the message.', 'nikhil.j@infowaysmedia.com', ['jadiyan@gmail.com'], fail_silently = False,)

    return render(request, 'forgot_password.html', context)


def reset_password(request):
    context = {}
    if request.method == 'POST':
        password = request.POST['txtPassword']
        confirm_password = request.POST['txtConfirmPassword']
        if password != "" and confirm_password != "":
            users = User.objects.all()
            user = users[0]
            user.set_password(password)
            user.save()
            context['message'] = 'Password reset successfully, Login again.'
        else:
            context['message'] = 'Password could not reset, Try again.'

    return render(request, 'reset_password.html', context)

############################################## TESTING AREA ##############################################

def test_template(request):
    context = {}
    d1 = datetime(2017, 8, 1)
    d2 = datetime(2017, 8, 8)
    delta = d2 - d1

    for i in range(delta.days + 1):
        print(d1 + timedelta(days=i))

    context['days'] = delta.days

    return render(request, 'test.html', context)


def test_url(request, action, employee_id):
    return HttpResponse(action + "Working.." + employee_id)
