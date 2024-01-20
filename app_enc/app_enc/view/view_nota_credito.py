import json
from inertia import render
from django.http import HttpResponse,JsonResponse
from django.middleware.csrf import get_token
from ..services.service_nota_credito import ServiceNotaCredito
from ..services.service_dynamics import ServiceDynamics

ServiceNotaCredito = ServiceNotaCredito
serviceDynamics = ServiceDynamics()

class ViewNotaCredito:
    def create_nota_credito(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("",request.POST)
            # form_request = json.loads(form_request)
            print('LLego a view')
            try:
                ServiceNotaCredito.crear_nota_credito(form_request)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)