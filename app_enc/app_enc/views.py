from inertia import render
from django.http import HttpResponse
    
# Ruta Index
def index(request):
    lista = []
    lista.append(12)
    return render(request,'Index',props={
        'array': lista
    })

# Ruta para login sesion
def login_successful(request):
    return HttpResponse("Hey, login successful.")