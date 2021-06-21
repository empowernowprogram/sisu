from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Player, Employer, PlaySession, ModuleDownloadLink, ComparisonRating, Adjective, SelectedAdjective, PostProgramSurvey

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer', 'supervisor', 'admin')


class PlaySessionAdmin(admin.ModelAdmin):
    list_display = ('player', 'module_id', 'success')

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'id')


class ModuleDownloadLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'training_type', 'platform_category', 'is_supervisor')


class PostProgramSurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'has_completed', 'overall_rating', 'creation_date')

class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ('adj_id', 'description')

class ComparisonRatingAdmin(admin.ModelAdmin):
    list_display = ('comparison_rating_id', 'description')

class SelectedAdjectiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(PlaySession, PlaySessionAdmin)
admin.site.register(ModuleDownloadLink, ModuleDownloadLinkAdmin)
admin.site.register(PostProgramSurvey, PostProgramSurveyAdmin)
admin.site.register(Adjective, AdjectiveAdmin)
admin.site.register(ComparisonRating, ComparisonRatingAdmin)
admin.site.register(SelectedAdjective, SelectedAdjectiveAdmin)
