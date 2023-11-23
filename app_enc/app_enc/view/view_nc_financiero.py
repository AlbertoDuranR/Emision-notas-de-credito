from inertia import render
from django.http import HttpResponse,JsonResponse
from ..services.service_nc_financiero import ServiceNCFinanciero
from ..services.service_dynamics import ServiceDynamics
import json

serviceFinanciero = ServiceNCFinanciero
serviceDynamics = ServiceDynamics()

class ViewNCFinanciero:
    ### Formulario Financieros
    def notaFinanciero(request):
        lista = []
        lista.append(12)
        #
        lista_markets= serviceFinanciero.get_all_markets()
        #
        return render(request,'NotaFinancieros',props={
            'lista_markets': lista_markets
        })
    
    ### Consolidado Financieros
    def cnotaFinanciero(request):
        lista = []
        lista.append(12)
        return render(request,'CNotaFinancieros',props={
            'array': lista
        })
    
    ### Bandeja Financieros
    def bnotaFinanciero(request):
        lista = []
        lista.append(12)
        return render(request,'BNotaFinancieros',props={
            'array': lista
        })
    
    ### Crear solicitud Financieras
    def create_solicitud_financieras(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("",request.POST)
            form_request = json.loads(form_request)
            #
            try:
                serviceFinanciero.save_solicitud(form_request)
                print("respondiendo")
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)    
            #
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)