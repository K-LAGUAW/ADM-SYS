from rest_framework import viewsets
from .models import Shipments
from .serializers import ShipmentsSerializer

class ShipmentsViewSet(viewsets.ModelViewSet):
    queryset = Shipments.objects.all().order_by('-creation_date')
    serializer_class = ShipmentsSerializer