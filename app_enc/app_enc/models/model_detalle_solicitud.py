from django.db import models

class DetalleSolicitud(models.Model):
    det_id = models.AutoField(primary_key=True)
    det_fecha_emision = models.DateField()
    det_nro_comprobante = models.CharField(max_length=64)
    det_importe_total = models.FloatField()
    det_motivo = models.CharField(max_length=255, null=True)
    det_justificacion = models.TextField(null=True)
    det_metodo = models.TextField(null=True)
    det_monto_total_prod = models.FloatField(null=True)
    det_establecimiento = models.IntegerField(null=True)
    det_descuento = models.IntegerField(null=True)
    det_total_descuento = models.FloatField(null=True)
    det_boleteo = models.FloatField(null=True)
    sdet_id = models.IntegerField(null=True)
    det_labora_en = models.CharField(max_length=64, null=True)
    sol_id = models.IntegerField(null=True)
    class Meta:
        db_table="detalle_solicitud"
        app_label="app_enc"