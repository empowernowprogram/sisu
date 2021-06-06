from rest_framework import serializers
from .models import Player, Employer, Modules, PlaySession, Employee

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ('email', 'employer', 'full_name')

class PlaySessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlaySession
        fields = ('employee_email', 'module_id', 'date_taken', 'score', 'success', 'time_taken')

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', 'password')
