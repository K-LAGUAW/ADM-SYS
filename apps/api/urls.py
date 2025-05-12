from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipmentsViewSet, PackageCategoriesViewSet

router = DefaultRouter()
router.register(r'shipments', ShipmentsViewSet, basename='shipments')
router.register(r'packages', PackageCategoriesViewSet, basename='packages')

urlpatterns = [
    path('', include(router.urls)),
]