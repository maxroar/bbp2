from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User
from datetime import datetime, timedelta, date
from django.forms.fields import DateTimeField

# Create your models here.
class AppointmentManager(models.Manager):
    def create_appointment(self, postData, user_id):
        date_app = postData['date_val']
        time_app = postData['time_val']
        app_date = datetime(year=int(date_app[0:4]), month=int(date_app[5:7]), day=int(date_app[8:10]), hour=int(time_app[0:2]), minute=int(time_app[3:5]))

        name = postData['content']
        self.create(name=name, user=User.objects.get(id=user_id), time=app_date, status='pending')

    def validate_app(self, postData):
        errors = []
        if len(postData['content']) < 3:
            errors.append('Appointments must be at least 3 characters long.')
        if not postData['date_val']:
            errors.append('Please enter a date.')
        if not postData['time_val']:
            errors.append('Please enter a time.')
        return errors

    def get_all_data(self, user_id):
        current_user = User.objects.get_user_data_from_session(user_id)
        other_apps = self.get_other_appointments(user_id)
        today_app = self.get_today_app(user_id)
        all_data = {
            'today_app': today_app,
            'other_apps': other_apps,
            'current_user': current_user
        }
        print all_data
        return all_data

    def get_today_app(self, user_id):
        today = date.today()
        # today_min = datetime.combine(today, datetime.time.min)
        # today_max = datetime.combine(today, datetime.time.max)
        # print(today_dt)
        return self.filter(user__id=user_id).filter(time__year=today.year, time__month=today.month, time__day=today.day)

    def get_other_appointments(self, user_id):
        today = date.today()
        return self.filter(user__id=user_id).exclude(time__year=today.year, time__month=today.month, time__day=today.day)

    def get_appointment_data(self, appointment_id):
        appointment_data = self.get(id=appointment_id)
        print appointment_data
        return appointment_data

    def is_user(self, appointment_id, user_id):
        is_true = self.filter(id=appointment_id,user=User.objects.get(id=user_id))
        return is_true

    def update_appointment(self, postData, appointment_id):
        date_app = postData['date_val']
        time_app = postData['time_val']
        app_date = datetime(year=int(date_app[0:4]), month=int(date_app[5:7]), day=int(date_app[8:10]), hour=int(time_app[0:2]), minute=int(time_app[3:5]))
        content=postData['content']
        status = postData['status']
        self.filter(id=appointment_id).update(name=content, status=status, time=app_date)

    def delete_appointment(self, postData, appointment_id):
        self.filter(id=appointment_id).delete()


class Appointment(models.Model):
    enum_choices = (
        ('p', 'pending'),
        ('d', 'done'),
        ('m', 'missed')
    )
    name = models.CharField(max_length=150)
    time = models.DateTimeField(auto_now=False)
    status = models.CharField(max_length=1, choices=enum_choices)
    user = models.ForeignKey(User, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()
