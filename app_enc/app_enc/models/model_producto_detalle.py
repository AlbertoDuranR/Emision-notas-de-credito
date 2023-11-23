from django.db import models

class ProductoDetalle(models.Model):
    dpro_id = models.AutoField(primary_key=True)
    dpro_codigo = models.CharField(max_length=7)
    dpro_descripcion = models.CharField(max_length=255)
    dpro_unidad = models.CharField(max_length=32)
    dpro_precio = models.FloatField()
    dpro_cantidad = models.IntegerField()
    dpro_monto_total = models.FloatField()
    det_id = models.IntegerField(null=True)
    class Meta:
        db_table="producto_detalle"
        app_label="app_enc"