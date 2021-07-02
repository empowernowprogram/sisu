# users/models.py
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user',on_delete=models.CASCADE)
    photo = models.CharField(max_length=255, blank=True, default='default_user')
    

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=CustomUser)