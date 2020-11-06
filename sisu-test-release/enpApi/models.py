from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    employer = models.IntegerField()
    full_name = models.CharField(max_length=60)
    supervisor = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
            on_delete=models.DO_NOTHING,
            null=True)

    def __str__(self):
        return self.email

class Employer(models.Model):
    company_name = models.CharField(max_length=60)

class Modules(models.Model):
    code = models.CharField(max_length=10)
    case = models.IntegerField()
    creation_date = models.DateField()

class PlaySession(models.Model):
    employer = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING, null=True)
    module_id = models.IntegerField()
    date_taken = models.DateField(auto_now=True)
    score = models.IntegerField()
    success = models.BooleanField()
    time_taken = models.IntegerField()
    
class LoginSessions(models.Model):
    email = models.CharField(max_length=50)
    date_logged_in = models.DateField(auto_now=True)

class Employee(models.Model):
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=30)

class Invite(models.Model):
    employer = models.IntegerField()
    email = models.CharField(max_length=50)
    link = models.CharField(max_length=30, primary_key=True)

