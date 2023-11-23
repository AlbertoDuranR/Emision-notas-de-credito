from django.db import models

class MenuRPermisos(models.Model):
    merp_id = models.AutoField(primary_key=True)
    men_id = models.IntegerField()
    rper_id = models.IntegerField()
    class Meta:
        db_table="menu_rpermisos"
        app_label="app_enc"