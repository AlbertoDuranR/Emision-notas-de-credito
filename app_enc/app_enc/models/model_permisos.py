from django.db import models

class Permisos(models.Model):
    per_id = models.AutoField(primary_key=True)
    per_codigo = models.CharField(max_length=5)
    per_descripcion = models.CharField(max_length=32)
    class Meta:
        db_table="permisos"
        app_label="app_enc"