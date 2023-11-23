from django.db import models

class Market(models.Model):
    mar_id = models.AutoField(primary_key=True)
    mar_descripcion = models.CharField(max_length=64)
    class Meta:
        db_table="market"
        app_label="app_enc"