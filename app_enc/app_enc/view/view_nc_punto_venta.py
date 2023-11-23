import json
from inertia import render
from django.http import HttpResponse,JsonResponse
from django.middleware.csrf import get_token
from ..services.service_nc_punto_venta import ServiceNCPDV
from ..services.service_dynamics import ServiceDynamics

servicePDV = ServiceNCPDV
serviceDynamics = ServiceDynamics()

class ViewNCPDV:
    ### Formulario Punto de Venta
    def notaPDV(request):
        # Lógica para obtener productos y unidades desde el servicio Dynamics
        products_issues= serviceDynamics.getProductsIssued()
        unidades= serviceDynamics.getUnitsConversion()
        #print(products_issues)
        #
        return render(request,'NotaPDV',props={
            'productos': products_issues,
            'unidades':unidades,
            '_token':get_token(request)
        })
     
     ## Formulario Punto de ventas edit   
    def notaPDVEdit(request, id):
        # Lógica para obtener productos y unidades desde el servicio Dynamics
        products_issues= serviceDynamics.getProductsIssued()
        unidades= serviceDynamics.getUnitsConversion()
        #print(products_issues)
        #
        return render(request,'NotaPDVEdit',props={
            'productos': products_issues,
            'unidades':unidades,
            'id': id,
            '_token':get_token(request)
        })
    
    ### Consolidado Punto de Venta
    def cnotaPDV(request):
        #Listar Solicitudes
        lista_solicitudes= servicePDV.lista_solicitudes()
        #
        return render(request,'CNotaPDV',props={
            'lista_solicitudes':lista_solicitudes
        })
    
    ### Bandeja Punto de Venta
    def bnotaPDV(request):
        lista = []
        lista.append(12)
        return render(request,'BNotaPDV',props={
            'array': lista
        })
    

    ### Crear solicitud PDV
    def create_solicitud_pdv(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("",request.POST)
            form_request = json.loads(form_request)
            #
            try:
                servicePDV.save_solicitud(form_request)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)    
            #
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)