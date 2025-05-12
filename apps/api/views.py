from rest_framework import viewsets
from .models import Shipments, PackageCategories
from .serializers import ShipmentsSerializer, PackageCategoriesSerializer

class ShipmentsViewSet(viewsets.ModelViewSet):
    queryset = Shipments.objects.all().order_by('-creation_date')
    serializer_class = ShipmentsSerializer

class PackageCategoriesViewSet(viewsets.ModelViewSet):
    queryset = PackageCategories.objects.all()
    serializer_class = PackageCategoriesSerializer