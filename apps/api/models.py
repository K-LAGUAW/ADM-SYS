import uuid
from django.db import models

class Shipments(models.Model):
    STATES = [
        ("preparation", "En preparación"),
        ('transit', 'En tránsito'),
        ('branch', 'En sucursal'),
        ('delivered', 'Entregado'),
        ('canceled', 'Cancelado'),
    ]

    tracking_number = models.CharField(max_length=11, unique=True, editable=False, verbose_name="Número de seguimiento")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    status = models.CharField(choices=STATES, default='preparation', verbose_name="Estado")
    sender = models.CharField(max_length=100, verbose_name="Remitente")
    recipient = models.CharField(max_length=100, verbose_name="Destinatario")
    package_amount = models.PositiveIntegerField(null=True, blank=True, verbose_name="Importe de bultos")
    envelope_amount = models.PositiveIntegerField(null=True, blank=True, verbose_name="Importe de sobres")
    total_amount = models.PositiveIntegerField(null=True, blank=True, verbose_name="Importe total")

    class Meta:
        verbose_name = "envio"
        verbose_name_plural = "envios"

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = f"PAQ-{uuid.uuid4().hex[:10].upper()}"
        package = self.package_amount if self.package_amount is not None else Decimal('0')
        envelope = self.envelope_amount if self.envelope_amount is not None else Decimal('0')
        self.total_amount = package + envelope
        super().save(*args, **kwargs)

    def __str__(self):
        formatted_date = self.update_date.strftime("%Y-%m-%d %I:%M %p")
        return f"Envio {self.tracking_number} - {self.get_status_display()}, ultima actualizacion: {formatted_date}"