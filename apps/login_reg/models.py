from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from datetime import datetime, timedelta, date
from django.forms.fields import DateTimeField

# Create your models here.
class UserManager(models.Manager):
    def validate_reg(self, postData):
        REGEX_EMAIL = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')
        REGEX_PASS = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,20}$')
        # list to hold error messages
        errors = []

        bday_form = postData['birthday']
        birthday = date(year=int(bday_form[0:4]), month=int(bday_form[5:7]), day=int(bday_form[8:10]))
        today = date.today()

        if len(postData['first_name']) < 3:
            errors.append('Name must be at least 2 characters.')
        if not REGEX_EMAIL.match(postData['email']):
            errors.append('Please use a valid email.')
        if birthday > date.today():
            errors.append('Please enter your real birthday.')
        if not REGEX_PASS.match(postData['pass1']):
            errors.append('Password must be at least 8 characters and contain at least 1 of each: capital letter, lowercase letter, number, special character.')
        if not postData['pass1'] == postData['pass2']:
            errors.append('Passwords must match.')
        if not self.check_email(postData):
            errors.append('Email already in use.')
        return errors

    def check_email(self, postData):
        emails = User.objects.filter(email=postData['email'])
        if emails:
            return False
        return True

    def create_user(self, postData):
        bday_form = postData['birthday']
        birthday = datetime(year=int(bday_form[0:4]), month=int(bday_form[5:7]), day=int(bday_form[8:10]))

        User.objects.create(first_name=postData['first_name'], email=postData['email'],
        birthdate=birthday, password=bcrypt.hashpw(postData['pass1'].encode(), bcrypt.gensalt()))

    def login(self, postData):
        user_data = User.objects.filter(email=postData['email']).first()
        # print(user_obj)
        pwhash = user_data.password.encode()
        if pwhash == bcrypt.hashpw(postData['pass1'].encode(), pwhash):
            return True
        return False

    def set_session(self, postData):
        user_data = User.objects.filter(email=postData['email']).first()
        user_id = user_data.id
        return user_id

    def get_user_data_from_session(self, session_id):
        user_data = User.objects.filter(id=session_id).first()
        print(user_data)
        return user_data



class User(models.Model):
    first_name = models.CharField(max_length=80)
    birthdate = models.CharField(max_length=30)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
