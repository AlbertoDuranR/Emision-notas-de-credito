from django.db import models

class SolicitanteDet(models.Model):
    sdet_id = models.AutoField(primary_key=True)
    sdet_dni = models.CharField(max_length=10)
    sdet_materno = models.CharField(max_length=64)
    sdet_paterno = models.CharField(max_length=64)
    sdet_nombres = models.CharField(max_length=64)
    class Meta:
        db_table ="solicitante_det"
        app_label = "app_enc"