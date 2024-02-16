from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime

from ..bot.dynamics_bot.dynamics_page_bot import Dynamics_Bot
from ..models.model_solicitud_nc import SolicitudNC
from ..models.model_producto_detalle import ProductoDetalle
from ..models.model_detalle_solicitud import DetalleSolicitud
from ..models.model_view_solicitudes_nota_de_credito import ViewSolicitudNotaDeCredito
from ..services.service_dynamics import ServiceDynamics

serviceDynamics = ServiceDynamics()


class ServiceNotaCredito:

    def get_data_solicitud(self, sol_id):
        '''
            # obtener datos de Postgres y Dynamics:
            output:
            {
                'num_comprobante_origen': det_nro_comprobante,
                'num_pedido_origen': num_pedido_origen,
                'metodo': det_metodo,
                'almacen': cod_almacen,
                'productos': list_productos,
                'forma_pago': cod_forma_pago,
                'pago': temino_pago,
                'fecha_solicitud': sol_fecha_solicitud.strftime("%m/%d/%Y"), # 1/21/2024
                'monto_total_nota_credito': det_monto_total_prod, # Parcial: Monto del producto | Total: Monto total de comprobante
                'sol_tipo_nc': sol_tipo_nc,
                'sol_estado': sol_estado
            }
        '''
        # Get data solicitud
        solicitud = ViewSolicitudNotaDeCredito.objects.get(sol_id=sol_id)
        if solicitud:
            sol_id = solicitud.sol_id
            det_id = solicitud.det_id
            sol_fecha_solicitud = solicitud.sol_fecha_solicitud
            sol_tipo_nc = solicitud.sol_tipo_nc
            sol_estado = solicitud.sol_estado
            det_nro_comprobante = solicitud.det_nro_comprobante
            det_metodo = solicitud.det_metodo
            det_monto_total_prod = solicitud.det_monto_total_prod
        # print('solicitud: ', sol_id, sol_fecha_solicitud,  sol_tipo_nc, sol_estado, det_nro_comprobante, det_metodo, det_monto_total_prod )

        # Get productos
        list_productos = []
        if det_metodo == 'parcial':
            productos = ProductoDetalle.objects.filter(det_id=det_id)
            if not productos:
                raise 'Error: Sin productos para el N° Comprobante en el metodo Parcial'
            for producto in productos:
                list_productos.append({'codigo': producto.dpro_codigo, 'cantidad': producto.dpro_cantidad})
        elif det_metodo == 'total':
            invoice_products = serviceDynamics.get_sales_invoice_lines(invoice_number=det_nro_comprobante)
            if not invoice_products:
                raise 'Error: Sin productos para el N° Comprobante en el metodo Total'
            for product in invoice_products:
                list_productos.append({'codigo': product['ProductNumber'], 'cantidad':  product['InvoicedQuantity']})
        else:
            raise 'Error: metodo de solicitud no encontrado'

        # Get data de Dynamic
        invoice_headers = serviceDynamics.get_sales_invoice_headers_by_invoice_number(invoice_number=det_nro_comprobante)
        if not invoice_headers:
            raise 'Error: Sin datos para el comprobante de origen en Dynamics'
        num_pedido_origen=invoice_headers[0]['SalesOrderNumber']
        temino_pago=invoice_headers[0]['PaymentTermsName']
        print("num_pedido_origen: ", num_pedido_origen)
        # Get data de Dynamics
        sales_order_headers = serviceDynamics.get_sales_order_headers_by_sales_order_number(sales_order_number=num_pedido_origen)
        if not sales_order_headers:
            raise 'Error: sin datos para el pedido de origen en Dynamics'
        cod_almacen=sales_order_headers[0]['DefaultShippingWarehouseId']
        cod_forma_pago=sales_order_headers[0]['CustomerPaymentMethodName']

        return {
            # Datos para RPA
            'num_comprobante_origen': det_nro_comprobante,
            'num_pedido_origen': num_pedido_origen,
            'metodo': det_metodo,
            'almacen': cod_almacen,
            'productos': list_productos,
            'forma_pago': cod_forma_pago,
            'pago': temino_pago,
            'fecha_solicitud': sol_fecha_solicitud.strftime("%m/%d/%Y"), # 1/21/2024
            'monto_total_nota_credito': det_monto_total_prod, # Parcial: Monto del producto | Total: Monto total de comprobante
            'sol_tipo_nc': sol_tipo_nc,
            'sol_estado': sol_estado
        }

    def save_error_in_solicitudNC(self, sol_id, error_msg):
        solicitud_existente = SolicitudNC.objects.get(sol_id=sol_id)
        if solicitud_existente:
            solicitud_existente.sol_fecha_modificacion = datetime.now().date()
            solicitud_existente.sol_estado = 'ERROR'
            solicitud_existente.sol_observacion = error_msg
            solicitud_existente.save()

    def crear_nota_credito(self, sol_id):
        # ---- data Ejemplos ---
        # data_parcial={
        #     "num_comprobante_origen": 'BF02-00153614',
        #     "PaymentTermsName": 'CONT',
        #     # Sale del orden de pedido
        #     "SalesOrderNumber": "TRV-02755697",
        #     "DefaultShippingWarehouseId": 'MD04_SUC',
        #     "CustomerPaymentMethodName": 'FP015',
        #     'num_pedido_origen': 'TRV-02755697',
        #     'metodo': 'parcial',
        #     'almacen': 'MD04_SUC',
        #     'productos': [
        #         # {'codigo': '101196', 'cantidad': '1'}, # 'codigo : cantidad ayer  08-02-23 se creo con este codigo
        #         {'codigo': '103271', 'cantidad': '1'}  # para el ejemplo a Danni usar este codigo # 102287 | 101780 | 110633
        #     ],
        #     'forma_pago':'FP015',
        #     'pago': 'CONT',
        #     'fecha_solicitud': '1/21/2024',
        #     'monto_total_nota_credito': '2.4' # <--- Cambiar monto del producto
        # }
        data_solicitud = self.get_data_solicitud(sol_id=sol_id)
        print('Data_solicitud: \n', data_solicitud)
        if data_solicitud['sol_tipo_nc'] == 'PDV' and data_solicitud['sol_estado'] == 'VALIDADO':
            dynamics_bot = Dynamics_Bot()
            dynamics_bot.iniciar_sesion()
            estado_rpa = dynamics_bot.crear_nota_de_credito(data=data_solicitud)
            print('Estado RPA: ', estado_rpa)
            nro_pedido_nota_credito = estado_rpa['nro_pedido_venta_devolucion']
            if not nro_pedido_nota_credito:
                error_msg = 'No se encontro el Nro de pedido para la nota de crédito con en el RPA'
                self.save_error_in_solicitudNC(sol_id, error_msg=error_msg)
                raise ErrorNotaDeCredito(error_msg)
            # Verificar existencia de nro de pedido
            return_order_headers = serviceDynamics.get_return_order_headers_by_return_order_number(nro_pedido_nota_credito)
            if not return_order_headers:
                error_msg='No se encontro el Nro de pedido para la nota de crédito en Dynamics'
                self.save_error_in_solicitudNC(sol_id, error_msg=error_msg)
                raise ErrorNotaDeCredito(error_msg)
            detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
            detalle_existente.det_nro_pedido_nota_credito = nro_pedido_nota_credito
            detalle_existente.save()
            if estado_rpa['estado'] == 'ERROR': # Verificar que no existe errores
                self.save_error_in_solicitudNC(sol_id, error_msg=estado_rpa['error']['mensaje'])
                raise ErrorNotaDeCredito(estado_rpa['error']['mensaje'], ubicacion=estado_rpa['error']['donde'])
            # Verificar si se llego a facturar
            nro_nota_credito=''
            sales_invoice_headers = serviceDynamics.get_sales_invoice_headers_by_sales_order_number(nro_pedido_nota_credito)
            if not sales_invoice_headers:
                raise ErrorNotaDeCredito('No se encontro la factura para la nota de crédito en Dynamics')
            nro_nota_credito = sales_invoice_headers[0]['InvoiceNumber']
            if estado_rpa['estado'] == 'CREADO' and nro_nota_credito:
                # 1. ACTUALIZAMOS solicitud_nc
                solicitud_existente = SolicitudNC.objects.get(sol_id=sol_id)
                if solicitud_existente:
                    # Actualizar el registro existente en SolicitudNC
                    solicitud_existente.sol_fecha_modificacion = datetime.now().date()
                    solicitud_existente.sol_estado = 'CREADO'
                    solicitud_existente.save()
                # 2. actualizamos detalle_solicitud
                detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
                if detalle_existente:
                    # Actualizar DetalleSolicitud
                    detalle_existente.det_nro_nota_credito = nro_nota_credito
                    detalle_existente.save()
            # Buscar
            # /data/ReturnOrderHeaders?$count=true&$filter=ReturnOrderNumber eq 'TRV-02756520'

    def reintentar_crear_nota_credito(self, sol_id):
        res = {
            "estado": "PENDIENTE", # CREADO
            "nro_pedido_nota_credito": None,
            "nro_nota_credito": None,
            "error": None
        }
        detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
        if not detalle_existente:
            res['error']='Error: No se encontro el detalle solicitud'
            raise res
        if detalle_existente.det_nro_nota_credito:
            res['estado'] = 'CREADO'
            res['nro_nota_credito'] = detalle_existente.det_nro_nota_credito
            return res
        if detalle_existente.det_nro_pedido_nota_credito:
            nro_pedido_nota_credito = detalle_existente.det_nro_pedido_nota_credito
        sales_invoice_headers = serviceDynamics.get_sales_invoice_headers_by_sales_order_number(nro_pedido_nota_credito)
        if sales_invoice_headers:
            res['estado']='CREADO'
            nro_nota_credito = sales_invoice_headers[0]['InvoiceNumber']
            # 1. ACTUALIZAMOS solicitud_nc
            solicitud_existente = SolicitudNC.objects.get(sol_id=sol_id)
            if solicitud_existente:
                # Actualizar el registro existente en SolicitudNC
                solicitud_existente.sol_fecha_modificacion = datetime.now().date()
                solicitud_existente.sol_estado = res['estado']
                solicitud_existente.save()
            # 2. actualizamos detalle_solicitud
            detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
            if detalle_existente:
                detalle_existente.det_nro_nota_credito = nro_nota_credito
                detalle_existente.save()
                return

        return_order_headers = serviceDynamics.get_return_order_headers_by_return_order_number(nro_pedido_nota_credito)
        if not return_order_headers:
                res['error']='Error: No se encontro número de pedido de retorno'
                raise res
        nro_rma = return_order_headers[0]['RMANumber']
        data_solicitud = self.get_data_solicitud(sol_id=sol_id)
        print('reintentar_crear_nota: sol_id: ', sol_id, detalle_existente.det_nro_nota_credito, nro_rma, data_solicitud)
        dynamics_bot = Dynamics_Bot()
        dynamics_bot.iniciar_sesion()
        estado_rpa = dynamics_bot.reintentar_crear_nota_de_credito(data=data_solicitud, nro_rma=nro_rma)
        print('Estado RPA: ', estado_rpa)
        nro_pedido_nota_credito = estado_rpa['nro_pedido_venta_devolucion']
        # Verificar si se llego a facturar
        sales_invoice_headers = serviceDynamics.get_sales_invoice_headers_by_sales_order_number(nro_pedido_nota_credito)
        if not sales_invoice_headers:
            res['error']='Error: No existe la factura para la nota de crédito'
            raise res
        nro_nota_credito = sales_invoice_headers[0]['InvoiceNumber']
        if not (estado_rpa['estado'] == 'CREADO' and nro_nota_credito):
            raise estado_rpa
        # 1. ACTUALIZAMOS solicitud_nc
        solicitud_existente = SolicitudNC.objects.get(sol_id=sol_id)
        if solicitud_existente:
            # Actualizar el registro existente en SolicitudNC
            solicitud_existente.sol_fecha_modificacion = datetime.now().date()
            solicitud_existente.sol_estado = 'CREADO'
            solicitud_existente.save()
        # 2. actualizamos detalle_solicitud
        detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
        if detalle_existente:
            detalle_existente.det_nro_nota_credito = nro_nota_credito
            detalle_existente.save()


class ErrorNotaDeCredito(Exception):
    '''Class to custom Exception'''
    def __init__(self, message, ubicacion=''):
        self.message = message
        self.ubicacion =  ubicacion
        super().__init__(self.message)
