from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Modules, Player, Employer, PlaySession, ModuleDownloadLink, ComparisonRating, Adjective, SelectedAdjective, PostProgramSurvey, PostProgramSurveySupervisor, Behavior, SceneInfo, EthicalFeedback

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer', 'supervisor', 'admin', 'creation_date')


class PlaySessionAdmin(admin.ModelAdmin):
    list_display = ('player', 'module_id', 'success', 'date_taken')

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'id')


class ModuleDownloadLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'training_type', 'platform_category', 'is_supervisor')


class PostProgramSurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'has_completed', 'overall_rating', 'creation_date')

class PostProgramSurveySupervisorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'has_completed', 'creation_date')

class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ('adj_id', 'description')

class ComparisonRatingAdmin(admin.ModelAdmin):
    list_display = ('comparison_rating_id', 'description')

class SelectedAdjectiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

class BehaviorAdmin(admin.ModelAdmin):
    list_display = ('behavior_id', 'description')

class SceneInfoAdmin(admin.ModelAdmin):
    list_display = ('module', 'scene', 'is_mandatory', 'player_role')

class EthicalFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'scene', 'emotion', 'behavior_id', 'timestamp')

class ModulesAdmin(admin.ModelAdmin):
    list_display = ('code', 'creation_date', 'is_mandatory')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(PlaySession, PlaySessionAdmin)
admin.site.register(ModuleDownloadLink, ModuleDownloadLinkAdmin)
admin.site.register(PostProgramSurvey, PostProgramSurveyAdmin)
admin.site.register(PostProgramSurveySupervisor, PostProgramSurveySupervisorAdmin) 
admin.site.register(Adjective, AdjectiveAdmin)
admin.site.register(ComparisonRating, ComparisonRatingAdmin)
admin.site.register(SelectedAdjective, SelectedAdjectiveAdmin)
admin.site.register(Behavior, BehaviorAdmin)
admin.site.register(SceneInfo, SceneInfoAdmin)
admin.site.register(EthicalFeedback, EthicalFeedbackAdmin)
admin.site.register(Modules, ModulesAdmin)
