from rest_framework import serializers
from . models import Shipments, PackageCategories

class ShipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = {
            'id': instance.status.id,
            'description': instance.status.name
        }
        return representation

class PackageCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategories
        fields = '__all__'