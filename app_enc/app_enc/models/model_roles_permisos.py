from django.db import models

class RolesPermisos(models.Model):
    rper_id = models.AutoField(primary_key=True)
    rol_id = models.IntegerField()
    per_id = models.IntegerField()
    class Meta:
        db_table="roles_permisos"
        app_label="app_enc"