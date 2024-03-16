from django.db import models

class ViewSolicitudNotaDeCredito(models.Model):
    sol_id = models.IntegerField(null=False, primary_key=True)
    det_id = models.IntegerField(null=False)
    sol_fecha_solicitud = models.DateField()
    sol_tipo_nc = models.CharField(max_length=64, null=False)
    sol_estado = models.CharField(max_length=64, null=True)
    sol_step_rpa = models.CharField(max_length=45)
    det_nro_comprobante = models.CharField(max_length=64, null=False)
    det_metodo = models.TextField(null=True)
    det_monto_total_prod = models.FloatField(null=False)
    det_importe_total = models.FloatField()
    det_motivo = models.CharField(max_length=255, null=True)
    det_justificacion = models.TextField(null=True)
    det_nro_nota_credito = models.CharField(max_length=13)
    det_nro_pedido_nota_credito = models.CharField(max_length=12)
    sol_acepta = models.CharField(max_length=64, null=True)
    det_forma_pago =  models.CharField(max_length=6)
    det_termino_pago =  models.CharField(max_length=10)

    class Meta:
        managed = False # Esto indica a Django que no gestione la tabla (ya que es una vista)
        db_table="view_solicitudes_nota_de_credito"
        app_label ="app_enc"
