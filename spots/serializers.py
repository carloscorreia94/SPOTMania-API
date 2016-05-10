from rest_framework import serializers
from .models import Spot
from rest_framework.validators import UniqueValidator
from django.db.models import CharField

class SpotSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Spot
        fields = ('name', 'description', 'created_at', 'lat', 'lng', 'created_by')

class NearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ('name','created_by','description','lat','lng')