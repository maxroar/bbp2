from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Appointment, AppointmentManager
from datetime import datetime, timedelta, date
from django.forms.fields import DateTimeField
# Create your views here.
def index(request):
    print(request.session['user_id'])
    all_data = Appointment.objects.get_all_data(request.session['user_id'])
    context = {
        'data': all_data
    }
    return render(request, 'appointment/index.html', context)

def display_add_appointment(request):
    all_data = Appointment.objects.get_all_data(request.session['user_id'])
    context = {
        'data': all_data
    }
    return redirect('/')

def create_appointment(request):
    errors = Appointment.objects.validate_app(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('appointment_ns:index')

    date_app = request.POST['date_val']
    app_date = date(year=int(date_app[0:4]), month=int(date_app[5:7]), day=int(date_app[8:10]))

    # CHANGE THIS TO ADD EQUALS


    if app_date < date.today():
        messages.add_message(request, messages.ERROR, 'Appointments must be in the future.')
        return redirect('appointment_ns:index')
    Appointment.objects.create_appointment(request.POST, request.session['user_id'])
    return redirect('appointment_ns:index')


def view_appointment(request, appointment_id):
    app_data = Appointment.objects.get_appointment_data(appointment_id)
    app_date = app_data.time.date()
    app_time = app_data.time.time()
    print app_date
    print app_time
    context = {
        'data': app_data,
        'date': app_date,
        'time': app_time
    }
    print(app_time)
    return render(request, 'appointment/edit.html', context)
def update_appointment(request, appointment_id):
    Appointment.objects.update_appointment(request.POST, appointment_id)
    return redirect('appointment_ns:index')

def delete_appointment(request, appointment_id):
    Appointment.objects.delete_appointment(request.POST, appointment_id)
    return redirect('appointment_ns:index')
