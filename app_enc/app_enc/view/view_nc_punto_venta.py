import json
import logging
from inertia import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from ..services.service_nc_punto_venta import ServiceNCPDV
from ..services.service_dynamics import ServiceDynamics
from ..scrapers.acepta_page_bot.acepta_page_bot import AceptaScraper
from ..models.model_producto_detalle import ProductoDetalle
from ..models.model_view_solicitudes_nota_de_credito import ViewSolicitudNotaDeCredito
from ..models.model_market import Market


servicePDV = ServiceNCPDV
serviceDynamics = ServiceDynamics()

# Configurar el logging para mostrar mensajes en la consola
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Obtener el logger para el módulo actual (o elige un nombre específico)
logger = logging.getLogger(__name__)

class ViewNCPDV:
    ## Formulario Punto de Venta
    def notaPDV(request):
        selectMarket = request.GET.get('selectMarket')
        market = Market.get_market_by_department_number(selectMarket)
        unidades= serviceDynamics.getUnitsConversion()
        return render(request,'NotaPDV',props={
            'unidades':unidades,
            'selectMarket':market,
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

    def get_datos_solicitud(request, sol_id):
        # Get data solicitud
        solicitud = ViewSolicitudNotaDeCredito.objects.get(sol_id=sol_id)
        if solicitud:
            sol_id = solicitud.sol_id
            det_id = solicitud.det_id
            sol_fecha_solicitud = solicitud.sol_fecha_solicitud
            sol_tipo_nc = solicitud.sol_tipo_nc
            det_nro_comprobante = solicitud.det_nro_comprobante
            det_metodo = solicitud.det_metodo
            det_monto_total_prod = solicitud.det_monto_total_prod
            det_importe_total = solicitud.det_importe_total
            det_motivo = solicitud.det_motivo
            det_justificacion = solicitud.det_justificacion
            det_nro_nota_credito = solicitud.det_nro_nota_credito
            det_nro_pedido_nota_credito = solicitud.det_nro_pedido_nota_credito
        # print('solicitud: ', sol_id, det_id, sol_fecha_solicitud,  sol_tipo_nc, det_nro_comprobante, det_metodo, det_monto_total_prod, det_importe_total )

        # Get productos
        list_productos = []
        productos = ProductoDetalle.objects.filter(det_id=det_id)
        if det_metodo == 'parcial':
            productos = ProductoDetalle.objects.filter(det_id=det_id)
            if not productos:
                raise 'Error: Sin productos para el N° Comprobante en el metodo Parcial'
            for producto in productos:
                list_productos.append({'codigo': producto.dpro_codigo, 'descripcion': producto.dpro_descripcion, 'cantidad': producto.dpro_cantidad, 'unidad': producto.dpro_unidad, 'monto_total': producto.dpro_monto_total})
        data_response = {
            'sol_fecha_solicitud': sol_fecha_solicitud,
            'sol_tipo_nc': sol_tipo_nc,
            'det_nro_comprobante': det_nro_comprobante,
            'det_metodo': det_metodo,
            'det_importe_total': det_importe_total,
            'det_motivo': det_motivo,
            'det_justificacion':  det_justificacion,
            'det_nro_nota_credito': det_nro_nota_credito,
            'det_nro_pedido_nota_credito': det_nro_pedido_nota_credito,
            'productos': list_productos
        }
        if not solicitud:
            return JsonResponse({'error': 'No se encontro la solicitud'}, status=404)
        return JsonResponse(data_response, safe=False)

    def get_name_by_dni_and_department(request, dni, department_number):
        print('dni', dni, department_number)
        name_employee=''
        employees = serviceDynamics.get_positionsv2_by_personnel_number(dni)
        if not employees:
            return JsonResponse({'error': 'No se encontro el empleado'}, status=404)
        for employee in employees:
            if employee['DepartmentNumber'] == department_number:
                name_employee = employee['WorkerName']
        if not name_employee:
            return JsonResponse({'error': 'El empleado no pertenece al departamento'}, status=404)
        print('name_employee', name_employee)
        name_employee_list = name_employee.split()
        ap_paterno = name_employee_list[-2]
        ap_materno = name_employee_list[-1]
        nombres = ' '.join(name_employee_list[:-2])
        return JsonResponse({ 'nombres': nombres, 'ap_paterno': ap_paterno, 'ap_materno': ap_materno }, safe=False)

     ## Formulario Punto de ventas edit
    def notaPDVEdit(request, id, id_product):
        selectMarket = request.GET.get('selectMarket')
        market = Market.get_market_by_department_number(selectMarket)
        lista_productosEdit = []
        # Lógica para obtener productos y unidades desde el servicio Dynamics
        unidades= serviceDynamics.getUnitsConversion()
        # Lógica para obtener datos de la base de datos local registrados
        lista_solicitudesEdit=servicePDV.lista_solicitudesEdit(id)
        products_issues=serviceDynamics.get_sales_invoice_lines(lista_solicitudesEdit[0]['NUMERO_COMPROBANTE'])
        # si es de tipo parcial traer los productos
        if 'parcial' in lista_solicitudesEdit[0]['METODO']:
            lista_productosEdit=servicePDV.lista_productosEdit(id_product)

        print("LISTA DE PROPDUCTOS")
        print(id)
        print(id_product)
        print(lista_productosEdit)
        #
        return render(request,'NotaPDVEdit',props={
            'productos': products_issues,
            'unidades': unidades,
            'lista_solicitudesEdit': lista_solicitudesEdit,
            'lista_productosEdit': lista_productosEdit,
            'id': id,
            '_token': get_token(request),
            'selectMarket': market
        })

    ### Consolidado Punto de Venta
    def cnotaPDV(request):
        selectMarket = request.GET.get('selectMarket')
        market = Market.get_market_by_department_number(selectMarket)
        #Listar Solicitudes
        lista_solicitudes= servicePDV.lista_solicitudes()
        #
        return render(request,'CNotaPDV',props={
            'lista_solicitudes': lista_solicitudes,
            'selectMarket': market,
        })

    ### Bandeja Punto de Venta
    def bnotaPDV(request):
        # selectMarket = request.GET.get('selectMarket')
        # market = Market.get_market_by_department_number(selectMarket)
        market = None
        lista_solicitudes= servicePDV.lista_solicitudes()
        return render(request,'BNotaPDV',props={
            'lista_solicitudes':lista_solicitudes,
            'selectMarket': market,
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
                return JsonResponse({'message': f'{e}'}, status=404)
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
