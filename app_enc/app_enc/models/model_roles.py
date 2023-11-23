from django.db import models

class Roles(models.Model):
    rol_id = models.AutoField(primary_key=True)
    rol_codigo = models.CharField(max_length=5)
    rol_descripcion = models.CharField(max_length=32)
    class Meta:
        db_table="roles"
        app_label="app_enc"