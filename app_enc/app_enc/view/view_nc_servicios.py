from inertia import render
from django.http import HttpResponse,JsonResponse
import json
from ..services.service_nc_servicios import ServiceNCServicios

serviceServ = ServiceNCServicios

class ViewNCServicios:

    ### Formulario Servicios
    def notaServicios(request):
        lista = []
        lista.append(12)
        return render(request,'NotaServicios',props={
            'array': lista
        })
    
    ### Consolidado Servicios
    def cnotaServicios(request):
        lista_solicitudes=ServiceNCServicios.lista_solicitudes()
        return render(request,'CNotaServicios',props={
            'lista_solicitudes': lista_solicitudes
        })
    
    ### Bandeja Servicios
    def bnotaServicios(request):
        lista = []
        lista.append(12)
        return render(request,'BNotaServicios',props={
            'array': lista
        })
    
    ### Crear solicitud Servicios
    def create_solicitud_servicios(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("",request.POST)
            form_request = json.loads(form_request)
            #
            try:
                serviceServ.save_solicitud(form_request)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)    
            #
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)