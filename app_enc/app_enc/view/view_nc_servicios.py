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
        
    ### Formulario Servicios edit
    def notaServiciosEdit(request, id):
        #lista = []
        #lista.append(12)
        lista_solicitudesEdit=ServiceNCServicios.lista_solicitudesEdit(id)
        return render(request,'NotaServiciosEdit',props={
            'lista_solicitudesEdit': lista_solicitudesEdit,
            'id': id
        })
    
    ### Consolidado Servicios
    def cnotaServicios(request):
        lista_solicitudes=ServiceNCServicios.lista_solicitudes()
        return render(request,'CNotaServicios',props={
            'lista_solicitudes': lista_solicitudes
        })
    
    ### Bandeja Servicios
    def bnotaServicios(request):
        # lista = []
        # lista.append(12)
        lista_solicitudes=ServiceNCServicios.lista_solicitudes()
        return render(request,'BNotaServicios',props={
            'lista_solicitudes': lista_solicitudes
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
        
    ### Editar solicitud Servicios
    def edit_solicitud_servicios(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("",request.POST)
            form_request = json.loads(form_request)
            #
            try:
                serviceServ.edit_solicitud(form_request)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)    
            #
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)
        
    ### Eliminar consolidado punto de venta
    def delete_consolidado(request):
        if request.method == "POST":
            try:
                # Obtener el id del cuerpo de la solicitud
                data = json.loads(request.body.decode('utf-8'))
                item_id = data.get('id')
            

                serviceServ.delete_solicitud(item_id)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)
            

    ## validar
    def validar_solicitud(request):
        if request.method == "POST":
            # Transform data
            data = json.loads(request.body.decode('utf-8'))

            try:
                #print(data)
                serviceServ.validate_solicitud(data)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)    
             #
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)       

    def observar_solicitud(request):
        if request.method == "POST":
            # Transform data
            data = json.loads(request.body.decode('utf-8'))

            try:
                #print(data)
                serviceServ.save_observacion(data)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)    
             #    