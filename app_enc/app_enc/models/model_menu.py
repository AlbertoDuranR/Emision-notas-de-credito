from django.db import models

class Menu(models.Model):
    men_id = models.AutoField(primary_key=True)
    men_descripcion = models.CharField(max_length=32)
    class Meta:
        db_table="menu"
        app_label="app_enc"