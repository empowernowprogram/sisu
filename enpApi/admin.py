from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Player, Employer, PlaySession, ModuleDownloadLink

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer', 'supervisor', 'admin')


class PlaySessionAdmin(admin.ModelAdmin):
    list_display = ('player', 'module_id', 'success')

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'id')


class ModuleDownloadLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'training_type', 'platform_category', 'is_supervisor')



admin.site.register(Player, PlayerAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(PlaySession, PlaySessionAdmin)
admin.site.register(ModuleDownloadLink, ModuleDownloadLinkAdmin)
