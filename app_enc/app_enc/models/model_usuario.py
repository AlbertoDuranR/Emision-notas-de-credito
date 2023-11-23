from django.db import models

class Usuario(models.Model):
    usu_id = models.AutoField(primary_key=True)
    usu_nombre = models.CharField(max_length=32)
    usu_correo = models.CharField(max_length=64, null=True)
    mar_id = models.IntegerField(null=True)
    rol_id = models.IntegerField(null=True)
    class Meta:
        db_table="usuario"
        app_label ="app_enc"