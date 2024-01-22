import json
import logging
from inertia import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from ..services.service_nc_punto_venta import ServiceNCPDV
from ..services.service_dynamics import ServiceDynamics
from ..scrapers.acepta_page_bot.acepta_page_bot import AceptaScraper

servicePDV = ServiceNCPDV
serviceDynamics = ServiceDynamics()

# Configurar el logging para mostrar mensajes en la consola
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Obtener el logger para el módulo actual (o elige un nombre específico)
# logger = logging.getLogger(__name__)

class ViewNCPDV:
    ## Formulario Punto de Venta
    def notaPDV(request):
        unidades= serviceDynamics.getUnitsConversion()
        return render(request,'NotaPDV',props={
            'unidades':unidades,
            '_token':get_token(request)
        })

    def get_sales_invoice(request, nro_comprobante):
        invoice = serviceDynamics.get_sales_invoice_headers_by_invoice_number(nro_comprobante)
        print('get_sales_invoices', invoice)
        if not invoice:
            return JsonResponse({'error': 'No se encontro el N° Comprobante'}, status=404)
        return JsonResponse(invoice, safe=False)

    def get_sales_invoice_details(request, nro_comprobante):
        invoice_products = serviceDynamics.get_sales_invoice_lines(nro_comprobante)
        # print('get_sales_invoices_details', invoice_products)
        if not invoice_products:
            return JsonResponse({'error': 'No se encontro productos para el N° Comprobante'}, status=404)
        return JsonResponse(invoice_products, safe=False)

     ## Formulario Punto de ventas edit
    def notaPDVEdit(request, id, id_product):
        
        lista_productosEdit = []
        # Lógica para obtener productos y unidades desde el servicio Dynamics
        products_issues= serviceDynamics.getProductsIssued()
        unidades= serviceDynamics.getUnitsConversion()
        
        # Lógica para obtener datos de la base de datos local registrados
        lista_solicitudesEdit=servicePDV.lista_solicitudesEdit(id)
        
       
       # si es de tipo parical traer los productos 
        if 'Parcial' in lista_solicitudesEdit[0]['METODO']:            
            lista_productosEdit=servicePDV.lista_productosEdit(id_product)
        
        print("LISTA DE PROPDUCTOS") 
        print(id)
        print(id_product)
        print(lista_productosEdit)
        #
        return render(request,'NotaPDVEdit',props={
            'productos': products_issues,
            'unidades':unidades,
            'lista_solicitudesEdit': lista_solicitudesEdit,
            'lista_productosEdit': lista_productosEdit,
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
        #lista = []
        #lista.append(12)
        lista_solicitudes= servicePDV.lista_solicitudes()
        return render(request,'BNotaPDV',props={
            'lista_solicitudes':lista_solicitudes
        })
    

    ### Crear solicitud PDV
    def create_solicitud_pdv(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("", request.POST)
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

    ## Editar solicitud PDV
    def edit_solicitud_pdv(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("",request.POST)
            form_request = json.loads(form_request)
            #
            try:
                servicePDV.edit_solicitud(form_request)
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
            

                servicePDV.delete_solicitud(item_id)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)

    def validar_solicitud(request):
        if request.method == "POST":
            # Transform data
            data = json.loads(request.body.decode('utf-8'))
            nro_comprobante = data['nro_comprobante'] # 'BG02-00052743'
            sales_invoice = serviceDynamics.get_sales_invoice_headers_by_invoice_number(nro_comprobante)
            if not sales_invoice:
                data["observacion"] = "Comprobante de origen no se encontro en Dynamics365. Verificar Nro de Comprobante"
                servicePDV.save_observacion(data)
                # logger.warning(f'Estado Dynamics 365: Existe')
                return JsonResponse({'message': 'Comprobante de origen no se encontro en Dynamics365'}, status=404)
            # logger.info(f'Estado Dynamics 365: {sales_invoice}')

            aceptaScraper = AceptaScraper() # Creamos un Objeto - instancia
            estado_acepta = aceptaScraper.get_estado_por_comprobante(nro_comprobante)
            if not estado_acepta == 'ACEPTADO':
                # logger.warning(f'Estado Portal Acepta: {estado_acepta}')
                return JsonResponse({'message': 'Comprobante de origen no se encontra Aceptado en el Portal ACEPTA'}, status=404)
            # logger.info(f'Estado Dynamics 365: {estado_acepta}')

            try:
                servicePDV.validate_solicitud(data)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)

    def observar_solicitud_pdv(request):
        if request.method == "POST":
            # Transform data
            data = json.loads(request.body.decode('utf-8'))

            try:
                #print(data)
                servicePDV.save_observacion(data)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)    
             #    