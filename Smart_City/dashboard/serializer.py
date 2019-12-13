from rest_framework import serializers
from .models import RFIDChipReader

# Serialize data to JSON format
class RFIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFIDChipReader
        fields = '__all__'