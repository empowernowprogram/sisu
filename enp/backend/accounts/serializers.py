from rest_framework import serializers
from .models import User, Employee, Module, Session
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

class ModuleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Module
        fields = ('id', 'url', 'case', 'categories', 'creation_date')

class SessionSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Session
        fields = (
            'id', 'employee', 'module_id', 
            'date_taken', 'score', 'grade', 
            'pass_fail', 'ethics', 
        )



