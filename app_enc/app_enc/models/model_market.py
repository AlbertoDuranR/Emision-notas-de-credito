from django.db import models

class Market(models.Model):
    mar_id = models.AutoField(primary_key=True)
    mar_descripcion = models.CharField(max_length=64)
    department_number = models.CharField(max_length=4)

    class Meta:
        db_table="market"
        app_label="app_enc"

    def get_all_markets():
        return list(Market.objects.all())

    def get_market_by_department_number(department_number: str):
        ''' :return Obj
            Ejemplo Uso:
            market.department_number
        '''
        return Market.objects.get(department_number=department_number)