from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    employer = models.IntegerField()
    full_name = models.CharField(max_length=60)
    supervisor = models.BooleanField()
    admin = models.BooleanField(default=False)
    registration_type = models.CharField(default='', max_length=16)
    has_signed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.email

class Employer(models.Model):
    company_name = models.CharField(max_length=60)
    employer_id = models.IntegerField()

class Modules(models.Model):
    code = models.CharField(max_length=10)
    case = models.IntegerField()
    creation_date = models.DateField()
    is_available = models.BooleanField(default=False)
    is_mandatory = models.BooleanField(default=False)

class PlaySession(models.Model):
    employer = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
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

class EmailList(models.Model):
    email = models.CharField(max_length=80)

class PassWordKey(models.Model):
    key = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

class RegKey(models.Model):
    key = models.CharField(max_length=20)
    supervisor = models.BooleanField()
    training_type = models.CharField(default='', max_length=16)
    company_name = models.CharField(default='', max_length=60)
    training_duration = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

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


# ComparisonRating holds current available comparison rating options in the survey
class ComparisonRating(models.Model):
    comparison_rating_id = models.IntegerField()
    description = models.CharField(max_length=255, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.description

# Adjectives holds currently available adjectives user can choose in the survey
class Adjective(models.Model):
    adj_id = models.IntegerField(blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.description

# AdjectivesSelected holds every adjective user chose in the survey
class SelectedAdjective(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=False)
    adj_id = models.ManyToManyField(Adjective, blank=False, null=True)
    creation_date = models.DateField(auto_now_add=True, null=True)

# PostProgramSurvey holds user feedbacks in the post program survey
class PostProgramSurvey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=False)
    overall_rating = models.IntegerField(blank=False)
    overall_feedback = models.TextField(max_length=3000, null=True, blank=True)
    comparison_rating_id = models.ForeignKey(ComparisonRating, on_delete=models.DO_NOTHING, null=True, blank=True)
    comments = models.TextField(max_length=3000, null=True, blank=True)
    contact = models.TextField(max_length=3000, null=True, blank=True)
    has_completed = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True, null=True)

# PostProgramSurveySupervisor holds user (a supervisor) feedbacks in the post program survey
class PostProgramSurveySupervisor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=False)
    recommend_friend_scale = models.IntegerField(blank=False)
    recommend_friend_reason = models.TextField(max_length=3000, null=True, blank=True)
    info_retention_scale = models.IntegerField(blank=False)
    confidence_scale = models.IntegerField(blank=False)
    comparison_rating_id = models.ForeignKey(ComparisonRating, on_delete=models.DO_NOTHING, null=True, blank=True)
    recommend_manager_scale = models.IntegerField(blank=False)
    recommend_employee_scale = models.IntegerField(blank=False)
    comments = models.TextField(max_length=3000, null=True, blank=True)
    has_completed = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True, null=True)
