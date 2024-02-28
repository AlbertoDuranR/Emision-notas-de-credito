from inertia import render
from django.http import HttpResponse
from .services.service_nc_financiero import ServiceNCFinanciero
from .models.model_market import Market

# Ruta Index
def index(request):
    lista = []
    lista.append(12)
    markets = Market.get_all_markets()
    return render(request,'Index',props={
        'array': lista,
        'lista_markets': markets
    })

# Ruta para login sesion
def login_successful(request):
    return HttpResponse("Hey, login successful.")