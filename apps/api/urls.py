from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipmentsViewSet

router = DefaultRouter()
router.register(r'shipments', ShipmentsViewSet, basename='shipments')

urlpatterns = [
    path('', include(router.urls)),
]