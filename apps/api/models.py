import uuid
import math
from django.db import models    

class PaymentCategories(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias de pago"

    def __str__(self):
        return self.name

class StatusCategories(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias de estado"

    def __str__(self):
        return self.name

class Shipments(models.Model):
    tracking_number = models.CharField(max_length=11, unique=True, verbose_name="Número de seguimiento")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    status = models.ForeignKey(StatusCategories, on_delete=models.CASCADE, verbose_name="Estado")
    sender = models.CharField(max_length=100, verbose_name="Remitente")
    recipient = models.CharField(max_length=100, verbose_name="Destinatario")
    phone = models.CharField(max_length=10, verbose_name="Teléfono")
    package_amount = models.IntegerField(null=True, blank=True, verbose_name="Importe de bultos")
    envelope_amount = models.IntegerField(null=True, blank=True, verbose_name="Importe de sobres")
    package_pickups = models.IntegerField(null=True, blank=True, verbose_name="Recogida de paquetes")
    total_amount = models.IntegerField(null=True, blank=True, verbose_name="Importe total")
    payment_type = models.ForeignKey(PaymentCategories, on_delete=models.CASCADE, verbose_name="Tipo de pago")

    class Meta:
        verbose_name = "envio"
        verbose_name_plural = "envios"

    def save(self, *args, **kwargs):
        package = (self.package_amount or 0)
        envelope = int((self.envelope_amount or 0) * 0.1)
        pickups = (self.package_pickups or 0) * 2500

        total = package + envelope + pickups
        self.total_amount = math.ceil(int(total) / 100) * 100

        super().save(*args, **kwargs)

    def __str__(self):
        formatted_date = self.update_date.strftime("%Y-%m-%d %I:%M %p")
        return f"Envio {self.tracking_number} - {self.get_status_display()}, ultima actualizacion: {formatted_date}"