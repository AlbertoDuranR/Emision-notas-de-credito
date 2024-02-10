from django.db import models

class ViewSolicitudNotaDeCredito(models.Model):
    sol_id = models.IntegerField(null=False, primary_key=True)
    det_id = models.IntegerField(null=False)
    sol_fecha_solicitud = models.DateField()
    sol_tipo_nc = models.CharField(max_length=64, null=False)
    sol_estado = models.CharField(max_length=64, null=True)
    det_nro_comprobante = models.CharField(max_length=64, null=False)
    det_metodo = models.TextField(null=True)
    det_monto_total_prod = models.FloatField(null=False)
    class Meta:
        managed = False # Esto indica a Django que no gestione la tabla (ya que es una vista)
        db_table="view_solicitudes_nota_de_credito"
        app_label ="app_enc"
