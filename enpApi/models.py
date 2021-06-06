from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    registration_type_choices = (('Desktop', 'Desktop'), ('VR', 'VR'))
    
    email = models.CharField(max_length=50, primary_key=True)
    employer = models.IntegerField()
    full_name = models.CharField(max_length=60)
    supervisor = models.BooleanField()
    admin = models.BooleanField(default=False)
    registration_type = models.CharField(max_length=255, null=False, blank=False, choices=registration_type_choices)
    has_signed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

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
    training_type = models.CharField(default='', max_length=16)

    
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


class ModuleDownloadLink(models.Model):
    # holds download links for modules
    training_type_choices = (('Desktop', 'Desktop'), ('VR', 'VR'))
    training_category_choices = (('None', 'None'), ('Harassment Training', 'Harassment Training'))
    platform_category_choices = (('Windows', 'Windows'), ('Mac', 'Mac'), ('SteamVR', 'SteamVR'), ('Oculus Quest', 'Oculus Quest'))
    
    training_type = models.CharField(max_length=255, null=False, blank=False, choices=training_type_choices)
    training_category = models.CharField(max_length=255, null=False, blank=False, choices=training_category_choices)
    platform_category = models.CharField(max_length=255, null=False, blank=False, choices=platform_category_choices)
    download_link = models.CharField(max_length=554, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)

    is_supervisor = models.BooleanField(null=False, blank=False)

    class Meta:
        ordering = ['training_type', 'platform_category']
