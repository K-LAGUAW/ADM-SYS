from rest_framework import serializers
from . models import Shipments

class ShipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = '__all__'