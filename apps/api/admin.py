from django.contrib import admin
from .models import Shipments, StatusCategories, PaymentCategories, PackageCategories

@admin.register(PackageCategories)
class PackageCategoriesAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentCategories)
class PaymentCategoriesAdmin(admin.ModelAdmin):
    pass

@admin.register(StatusCategories)
class StatusCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Shipments)
class Shipments(admin.ModelAdmin):
    readonly_fields = ('qr_code', 'total_amount',)