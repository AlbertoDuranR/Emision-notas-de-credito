from django.db import models

class SolicitudNC(models.Model):
    ESTADO_CHOICES = [
        'PENDIENTE',
        'VALIDADO',
        'OBSERVADO',
        'ERROR',
        'ELIMINADO',
    ]
    ESTADO_RPA_CHOICES = [
        'PEDIDO', # al crear el pedido
        'ENLAZAR',
        'REGISTRAR',
        'VALIDAR',
        'FACTURAR'
    ]
    sol_id = models.AutoField(primary_key=True)
    sol_fecha_solicitud = models.DateField()
    sol_tipo_nc = models.CharField(max_length=64)
    sol_usuario_creador = models.IntegerField()
    sol_fecha_creacion = models.DateField(null=True)
    sol_fecha_modificacion = models.DateField(null=True)
    sol_estado = models.CharField(max_length=64, null=True, choices=ESTADO_CHOICES)
    sol_observacion = models.TextField(null=True)
    sol_usuario_validador = models.IntegerField(null=True)
    sol_step_rpa = models.CharField(max_length=45, choices=ESTADO_RPA_CHOICES)

    class Meta:
        db_table="solicitud_nc"
        app_label="app_enc"