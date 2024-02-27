from inertia import render
from django.http import HttpResponse
from .services.service_nc_financiero import ServiceNCFinanciero
    
# Ruta Index
def index(request):
    lista = []
    lista.append(12)
    serviceFinanciero = ServiceNCFinanciero
    lista_markets= serviceFinanciero.get_all_markets()

    return render(request,'Index',props={
        'array': lista,
        'lista_markets': lista_markets
    })

# Ruta para login sesion
def login_successful(request):
    return HttpResponse("Hey, login successful.")