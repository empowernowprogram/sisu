from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Modules(models.Model):
    module_id = models.CharField(max_length=10)
    creation_date = models.DateField()
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.module_id

class Employer(models.Model):
    employer_id = models.IntegerField(null=True) # do we need this
    company_name = models.CharField(max_length=60)
    logo = models.TextField(max_length=1000, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    deadline_duration_days = models.IntegerField(default=60)
    mandatory_modules = models.ManyToManyField(Modules, related_name='mandatory_modules', blank=True)
    registered_modules = models.ManyToManyField(Modules, related_name='all_modules', blank=True)

    def __str__(self):
        return self.company_name

class Player(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    employer = models.ForeignKey(Employer, on_delete=models.DO_NOTHING, null=True)
    
    full_name = models.CharField(max_length=60)
    supervisor = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    registration_type = models.CharField(default='', max_length=16)
    has_signed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    is_provisional = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=True, null=True)
    training_deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email

class SupervisorMapping(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='team_member', on_delete=models.CASCADE, null=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='team_supervisor', on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, null=True)
    modification_date = models.DateField(auto_now=True, null=True)

    class Meta:
        ordering = ['supervisor']

class PlaySession(models.Model):
    employer = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    module_id = models.CharField(max_length=10)
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

class TrainingPackageDownloadLink(models.Model):
    # holds download links for modules
    training_type_choices = (('Desktop', 'Desktop'), ('VR', 'VR'))
    training_category_choices = (('None', 'None'), ('Harassment Training', 'Harassment Training'))
    platform_category_choices = (('Windows', 'Windows'), ('Mac', 'Mac'), ('SteamVR', 'SteamVR'), ('Oculus Quest', 'Oculus Quest'))

    training_type = models.CharField(max_length=255, null=False, blank=False, choices=training_type_choices)
    training_category = models.CharField(max_length=255, null=False, blank=False, choices=training_category_choices)
    platform_category = models.CharField(max_length=255, null=False, blank=False, choices=platform_category_choices)
    download_link = models.CharField(max_length=554, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True, default='1.2GB')

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
    adj_id = models.ManyToManyField(Adjective, blank=False)
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
    recommend_friend_scale = models.IntegerField(null=True, blank=False)
    recommend_friend_reason = models.TextField(max_length=3000, null=True, blank=True)
    info_retention_scale = models.IntegerField(null=True, blank=False)
    confidence_scale = models.IntegerField(null=True, blank=False)
    comparison_rating_id = models.ForeignKey(ComparisonRating, on_delete=models.DO_NOTHING, null=True, blank=True)
    recommend_manager_scale = models.IntegerField(null=True, blank=False)
    recommend_employee_scale = models.IntegerField(null=True, blank=False)
    comments = models.TextField(max_length=3000, null=True, blank=True)
    has_completed = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True, null=True)

# Behavior holds available behavior: hostile/passive/confident
class Behavior(models.Model):
    behavior_id = models.IntegerField(blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.description

# SceneInfo (original name: PlayerRole) holds the role player plays in each scene
class SceneInfo(models.Model):
    module_id = models.CharField(max_length=10, blank=False) # should have relationship
    scene = models.IntegerField(blank=False)
    is_mandatory = models.BooleanField(default=True)
    player_role = models.CharField(max_length=255, blank=False)
    ethical_screenshot = models.TextField(max_length=1000, null=True, blank=True)
    ethical_npc_name = models.CharField(max_length=50, null=True, blank=True)
    ethical_script = models.TextField(max_length=1000, null=True, blank=True)

# EthicalFeedback holds user's ethical performance during training
class EthicalFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=False)
    module_id = models.CharField(max_length=10, blank=False) # should have relationship
    scene = models.IntegerField(blank=False)
    emotion = models.IntegerField(blank=False)
    behavior_id = models.ForeignKey(Behavior, on_delete=models.DO_NOTHING, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
