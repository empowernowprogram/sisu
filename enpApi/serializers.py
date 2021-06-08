from rest_framework import serializers
from .models import Player, Employer, Modules, PlaySession, Employee

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ('email', 'employer', 'full_name')

class PlaySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaySession
        fields = ('employer', 'player', 'module_id', 'date_taken', 'score', 'success', 'time_taken', 'training_type')

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', 'password')

class EmployerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('company_name', 'employer_id')

class ModulesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Modules
        fields = ('code', 'case', 'creation_date')

