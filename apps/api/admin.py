from django.contrib import admin
from .models import Shipments, StatusCategories, PaymentCategories

@admin.register(PaymentCategories)
class PaymentCategoriesAdmin(admin.ModelAdmin):
    pass

@admin.register(StatusCategories)
class StatusCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Shipments)
class Shipments(admin.ModelAdmin):
    readonly_fields = ('total_amount',)