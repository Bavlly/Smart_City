from rest_framework import serializers
from .models import RfidChipReader

class SensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RfidChipReader
        fields = '__all__'