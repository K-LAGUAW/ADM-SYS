import math
import uuid
import qrcode
from django.core.files.base import ContentFile
from django.db import models
from io import BytesIO

class PaymentCategories(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Nombre"
    )

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias de pago"

    def __str__(self):
        return self.name

class StatusCategories(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Nombre"
    )

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias de estado"

    def __str__(self):
        return self.name

class Shipments(models.Model):
    """
    Modelo para gestionar envíos con seguimiento, códigos QR y cálculos de costos.
    """
    ENVELOPE_RATE = 0.1
    PICKUP_RATE = 2500
    ROUNDING_STEP = 100
    TRACKING_PREFIX = "PAQ-"
    TRACKING_LENGTH = 7

    tracking_number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="Número de seguimiento",
        editable=False
    )
    qr_code = models.ImageField(
        upload_to='qrcodes/',
        blank=True,
        verbose_name="Código QR"
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    status = models.ForeignKey(
        'StatusCategories',
        on_delete=models.CASCADE,
        verbose_name="Estado",
        default=1
    )
    sender = models.CharField(
        max_length=100,
        verbose_name="Remitente"
    )
    recipient = models.CharField(
        max_length=100,
        verbose_name="Destinatario"
    )
    phone = models.CharField(
        max_length=10,
        verbose_name="Teléfono"
    )
    package_amount = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Importe de bultos"
    )
    envelope_amount = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Importe de sobres"
    )
    package_pickups = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Recogida de paquetes"
    )
    total_amount = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Importe total"
    )
    payment_type = models.ForeignKey(
        'PaymentCategories',
        on_delete=models.CASCADE,
        verbose_name="Tipo de pago"
    )

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"
        ordering = ['-creation_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_tracking_number = self.tracking_number

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar número de seguimiento,
        código QR y calcular el importe total antes de guardar.
        """
        self._generate_tracking_number()
        self._generate_qr_code()
        self._calculate_total_amount()
        super().save(*args, **kwargs)

    def _generate_tracking_number(self):
        """Genera un número de seguimiento único si no existe."""
        if not self.tracking_number:
            uuid_part = uuid.uuid4().hex[:self.TRACKING_LENGTH].upper()
            self.tracking_number = f"{self.TRACKING_PREFIX}{uuid_part}"

    def _generate_qr_code(self):
        """Genera un código QR para el número de seguimiento."""
        if self._tracking_changed() or not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.tracking_number)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            file_name = f"qr_{self.tracking_number}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

    def _tracking_changed(self):
        """Verifica si el número de seguimiento ha cambiado."""
        return self.tracking_number != self.__original_tracking_number

    def _calculate_total_amount(self):
        """Calcula el importe total del envío."""
        def get_value(field):
            return getattr(self, field) or 0
        
        base_calculation = (
            get_value('package_amount') +
            int(get_value('envelope_amount') * self.ENVELOPE_RATE) +
            (get_value('package_pickups') * self.PICKUP_RATE)
        )
        
        self.total_amount = math.ceil(base_calculation / self.ROUNDING_STEP) * self.ROUNDING_STEP

    def __str__(self):
        formatted_date = self.update_date.strftime("%Y-%m-%d %H:%M")
        return f"{self.tracking_number} - {self.status} | Actualizado: {formatted_date}"