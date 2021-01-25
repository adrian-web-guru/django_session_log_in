from rest_framework import serializers
from .models import AirplaneCollector

class AirplaneCollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneCollector
        fields = ('username', 'password')