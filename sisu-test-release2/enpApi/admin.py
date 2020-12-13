from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Player, Employer, PlaySession

admin.site.register(Player)
admin.site.register(Employer)
admin.site.register(PlaySession)
