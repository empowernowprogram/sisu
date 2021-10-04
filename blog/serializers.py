from rest_framework import serializers
from .models import DLinks

class DLinksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DLinks
        fields = ('training_type', 'supervisor', 'link_address')
