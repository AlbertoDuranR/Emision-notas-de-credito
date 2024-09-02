import os
import time
from datetime import datetime

from ..bot.dynamics_bot.dynamics_page_bot import Dynamics_Bot
from ..models.model_solicitud_nc import SolicitudNC
from ..models.model_producto_detalle import ProductoDetalle
from ..models.model_detalle_solicitud import DetalleSolicitud
from ..models.model_view_solicitudes_nota_de_credito import ViewSolicitudNotaDeCredito
from ..services.service_dynamics import ServiceDynamics

serviceDynamics = ServiceDynamics()
dynamics_bot = Dynamics_Bot()


class ServiceNotaCredito:

    def handle_data_rpa(self, estado_rpa, sol_id):
        if not estado_rpa['step_rpa']:
            raise ErrorNotaDeCredito(message='No se llego a crear el pedido. Reintentar')
        nro_pedido_nota_credito = estado_rpa['nro_pedido_venta_devolucion']
        if nro_pedido_nota_credito: # Si existe guardar el nro de pedido
            return_order_headers = serviceDynamics.get_return_order_headers_by_return_order_number(nro_pedido_nota_credito)
            if not return_order_headers:
                error_msg='No se encontro el Nro de pedido para la nota de crédito en Dynamics'
                raise ErrorNotaDeCredito(message=error_msg, estado=estado_rpa['estado'])
            print('Guardando Nro Pedido de Nota de Credito: ', nro_pedido_nota_credito)
            detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
            detalle_existente.det_nro_pedido_nota_credito = nro_pedido_nota_credito
            detalle_existente.save()
        if estado_rpa['estado'] == 'ERROR':
            raise ErrorNotaDeCredito(message=estado_rpa['error']['mensaje'], estado=estado_rpa['estado'], step=estado_rpa['step_rpa'])
        self.save_nota_de_credito(sol_id, estado_rpa, nro_pedido_nota_credito)

    def crear_masivo_notas_de_credito(self, sol_ids):
        print('crear_masivo_notas_de_credito, sol_ids:', sol_ids)
        data_solicitudes = [] # [{} , {}, {}]
        for sol_id in sol_ids:
            data_solicitud = self.get_data_solicitud(sol_id=sol_id)
            data_solicitudes.append(data_solicitud)
            print(data_solicitudes)

        # estados_rpa = [] # [{}, {}, {}]
        dynamics_bot.init_navigator()
        dynamics_bot.ir_a_url_inicial()
        dynamics_bot.iniciar_sesion()
        for data in data_solicitudes:
            try:
                print(f'Crear Data {data}, {data["sol_id"]}')
                estado_rpa = dynamics_bot.crear_nota_de_credito(data)
                # estados_rpa.append(estado_rpa)
                print(f'Estado RPA: {estado_rpa}')
                self.handle_data_rpa(estado_rpa=estado_rpa, sol_id=estado_rpa['sol_id'])
                time.sleep(1)
                dynamics_bot.ir_a_url_inicial()
                time.sleep(1)
            except ErrorNotaDeCredito as e:
                print('Error al manejar data RPA al crear masivo', e.estado, e.message, e.step)
                self.save_error_in_solicitudNC(sol_id=estado_rpa['sol_id'], estado_error=e.estado, error_msg=e.message, step_rpa=e.step)
                break
        dynamics_bot.close_driver()

    # Deprecated: Ahora se indicara que hacer al bot en todo momento desde service_nota_credito
    # def crear_masivo_notas_de_credito(self, sol_ids):
    #     print('crear_masivo_notas_de_credito, sol_ids:', sol_ids)
    #     data_solicitudes = [] # [{} , {}, {}]
    #     for sol_id in sol_ids:
    #         data_solicitud = self.get_data_solicitud(sol_id=sol_id)
    #         data_solicitudes.append(data_solicitud)
    #         print(data_solicitudes)

    #     # crear  NC uno por uno
    #     estados_rpa=dynamics_bot.crear_masivo_nota_de_credito(data_solicitudes=data_solicitudes)
    #     print(f'Estados rpa: {estados_rpa}')
    #     for estado_rpa in estados_rpa:
    #         try:
    #             self.handle_data_rpa(estado_rpa=estado_rpa, sol_id=estado_rpa['sol_id'])
    #         except ErrorNotaDeCredito as e:
    #             print('Error al manejar data RPA al crear masivo', e.estado, e.message, e.step)
    #             self.save_error_in_solicitudNC(sol_id=estado_rpa['sol_id'], estado_error=e.estado, error_msg=e.message, step_rpa=e.step)

    def crear_nota_credito(self, sol_id):
        '''
        ---- data Ejemplos ---
        data_parcial={
            "num_comprobante_origen": 'BF02-00153614',
            "PaymentTermsName": 'CONT',
            # Sale del orden de pedido
            "SalesOrderNumber": "TRV-02755697",
            "DefaultShippingWarehouseId": 'MD04_SUC',
            "CustomerPaymentMethodName": 'FP015',
            'num_pedido_origen': 'TRV-02755697',
            'metodo': 'parcial',
            'almacen': 'MD04_SUC',
            'productos': [
                # {'codigo': '101196', 'cantidad': '1'}, # 'codigo : cantidad ayer  08-02-23 se creo con este codigo
                {'codigo': '103271', 'cantidad': '1'}  # para el ejemplo a Danni usar este codigo # 102287 | 101780 | 110633
            ],
            'forma_pago':'FP015',
            'pago': 'CONT',
            'fecha_solicitud': '1/21/2024',
            'monto_total_nota_credito': '2.4' # <--- Cambiar monto del producto
        }
        '''
        data_solicitud = self.get_data_solicitud(sol_id=sol_id)
        print('Data_solicitud: \n', data_solicitud)
        if data_solicitud['sol_tipo_nc'] == 'PDV' and data_solicitud['sol_estado'] == 'VALIDADO':
            estado_rpa = dynamics_bot.crear_individual_nota_de_credito(data=data_solicitud)
            print(f'Estado sol_id {sol_id} RPA:  {estado_rpa}')
            try:
                self.handle_data_rpa(estado_rpa=estado_rpa, sol_id=sol_id)
            except ErrorNotaDeCredito as e:
                print('Error al manejar data RPA al crear', e, e.estado, e.message, e.step)
                self.save_error_in_solicitudNC(sol_id=sol_id, estado_error=e.estado, error_msg=e.message, step_rpa=e.step)
                raise e

    def reintentar_crear_nota_credito(self, sol_id):
        detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
        if not detalle_existente:
            error_msg=f'No se encontro detalle solicitud para el sol_id {sol_id}'
            self.save_error_in_solicitudNC(sol_id, error_msg=error_msg)
            raise ErrorNotaDeCredito(error_msg)
        if detalle_existente.det_nro_nota_credito:
            # Verifica si ya existe la factura de nota de crédito
            return

        if not detalle_existente.det_nro_pedido_nota_credito:
            error_msg=f'No se encontro el número de pedido de nota de credito'
            self.save_error_in_solicitudNC(sol_id, error_msg=error_msg)
            raise ErrorNotaDeCredito(error_msg)

        nro_pedido_nota_credito = detalle_existente.det_nro_pedido_nota_credito
        # Verifica si existe la factura de la nota de credito
        sales_invoice_headers = serviceDynamics.get_sales_invoice_headers_by_sales_order_number(nro_pedido_nota_credito)
        if sales_invoice_headers:
            nro_nota_credito = sales_invoice_headers[0]['InvoiceNumber']
            solicitud_existente = SolicitudNC.objects.get(sol_id=sol_id)
            if solicitud_existente:
                solicitud_existente.sol_fecha_modificacion = datetime.now().date()
                solicitud_existente.sol_estado = 'CREADO'
                solicitud_existente.save()
            detalle_existente = DetalleSolicitud.objects.get(sol_id=sol_id)
            if detalle_existente:
                detalle_existente.det_nro_nota_credito = nro_nota_credito
                detalle_existente.save()
                return

        # START get nro RMA
        return_order_headers = serviceDynamics.get_return_order_headers_by_return_order_number(nro_pedido_nota_credito)
        if not return_order_headers:
            error_msg=f'No se encontro el pedido de retorno'
            self.save_error_in_solicitudNC(sol_id, error_msg=error_msg)
            raise ErrorNotaDeCredito(error_msg)
        if return_order_headers[0]['ReturnOrderStatus'].lower() == 'canceled':
            error_msg = f'Verificar si el pedido de devolución {nro_pedido_nota_credito} esta Cancelado en Dynamics. Proceder a eliminar la solicitud y crear uno nuevo'
            print(error_msg)
            raise ErrorNotaDeCredito(error_msg)

        nro_rma = return_order_headers[0]['RMANumber']
        # End get nro RMA

        # START Reintentar
        data_solicitud = self.get_data_solicitud(sol_id=sol_id)
        print('Data_solicitud: \n', data_solicitud, '\n nro_rma: ', nro_rma)
        estado_rpa = dynamics_bot.reintentar_crear_nota_de_credito(data=data_solicitud, nro_rma=nro_rma, nro_pedido_nota_credito=nro_pedido_nota_credito)
        print('Estado RPA: ', estado_rpa, estado_rpa['step_rpa'])
        try:
            self.handle_data_rpa(estado_rpa=estado_rpa, sol_id=sol_id)
        except ErrorNotaDeCredito as e:
            print('Error al manejar data RPA al reintentar', e.estado, e.message, e.step)
            self.save_error_in_solicitudNC(sol_id=sol_id, estado_error=e.estado, error_msg=e.message, step_rpa=e.step)
            raise e

    def save_nota_de_credito(self, sol_id, estado_rpa, nro_pedido_nota_credito):
        # Verificar si se llego a facturar
        nro_nota_credito=''
        sales_invoice_headers = serviceDynamics.get_sales_invoice_headers_by_sales_order_number(nro_pedido_nota_credito)
        count = 0
        while sales_invoice_headers == None:
            time.sleep(5)
            sales_invoice_headers = serviceDynamics.get_sales_invoice_headers_by_sales_order_number(nro_pedido_nota_credito)
            if sales_invoice_headers:
                break
            count += 1
            if count > 1:
                msg_error = f'No se encontro la factura para la nota de crédito en Dynamics. Para el pedido : {nro_pedido_nota_credito}'
                self.save_error_in_solicitudNC(sol_id, estado_error='ERROR', error_msg=msg_error, step_rpa=estado_rpa['step_rpa'])
                raise ErrorNotaDeCredito(message=msg_error)

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
            sol_step_rpa = solicitud.sol_step_rpa
            det_nro_comprobante = solicitud.det_nro_comprobante
            det_metodo = solicitud.det_metodo
            det_monto_total_prod = solicitud.det_monto_total_prod
            det_forma_pago = solicitud.det_forma_pago
            det_termino_pago = solicitud.det_termino_pago
        # print('solicitud: ', sol_id, sol_fecha_solicitud,  sol_tipo_nc, sol_estado, det_nro_comprobante, det_metodo, det_monto_total_prod )

        # Get productos
        list_productos = []
        if det_metodo == 'parcial':
            productos = ProductoDetalle.objects.filter(det_id=det_id)
            if not productos:
                raise ErrorNotaDeCredito(message='Error: Sin productos para el N° Comprobante en el metodo Parcial')
            for producto in productos:
                list_productos.append({'codigo': producto.dpro_codigo, 'cantidad': producto.dpro_cantidad})
        elif det_metodo == 'total':
            invoice_products = serviceDynamics.get_sales_invoice_lines(invoice_number=det_nro_comprobante)
            if not invoice_products:
                raise ErrorNotaDeCredito(message='Error: Sin productos para el N° Comprobante en el metodo Total')
            for product in invoice_products:
                list_productos.append({'codigo': product['ProductNumber'], 'cantidad':  product['InvoicedQuantity']})
        else:
            raise ErrorNotaDeCredito(message='Error: metodo de solicitud no encontrado')

        # Get data de Dynamic
        invoice_headers = serviceDynamics.get_sales_invoice_headers_by_invoice_number(invoice_number=det_nro_comprobante)
        if not invoice_headers:
            raise ErrorNotaDeCredito(message='Error: Sin datos para el comprobante de origen en Dynamics')
        num_pedido_origen=invoice_headers[0]['SalesOrderNumber']
        # termino_pago=invoice_headers[0]['PaymentTermsName']
        print("num_pedido_origen: ", num_pedido_origen)
        # Get data de Dynamics
        sales_order_headers = serviceDynamics.get_sales_order_headers_by_sales_order_number(sales_order_number=num_pedido_origen)
        if not sales_order_headers:
            raise ErrorNotaDeCredito(message='Error: sin datos para el pedido de origen en Dynamics')
        cod_almacen=sales_order_headers[0]['DefaultShippingWarehouseId']
        # cod_forma_pago=sales_order_headers[0]['CustomerPaymentMethodName']

        return {
            # Datos para RPA
            'num_comprobante_origen': det_nro_comprobante,
            'num_pedido_origen': num_pedido_origen,
            'metodo': det_metodo,
            'almacen': cod_almacen,
            'productos': list_productos,
            'forma_pago': det_forma_pago,
            'pago': det_termino_pago,
            'fecha_solicitud': sol_fecha_solicitud.strftime("%d/%m/%Y"), # 27/02/2024
            'monto_total_nota_credito': det_monto_total_prod, # Parcial: Monto del producto | Total: Monto total de comprobante
            'sol_tipo_nc': sol_tipo_nc,
            'sol_estado': sol_estado,
            'step_rpa': sol_step_rpa,
            'sol_id': sol_id
        }

    def save_error_in_solicitudNC(self, sol_id: str, estado_error='', error_msg='', step_rpa = ''):
        print('save_error_in_solicitudNC')
        solicitud_existente = SolicitudNC.objects.get(sol_id=sol_id)
        if solicitud_existente:
            solicitud_existente.sol_fecha_modificacion = datetime.now().date()
            solicitud_existente.sol_estado = 'ERROR' if estado_error == 'ERROR' else solicitud_existente.sol_estado
            solicitud_existente.sol_observacion = error_msg
            solicitud_existente.sol_step_rpa = step_rpa
            solicitud_existente.save()


class ErrorNotaDeCredito(Exception):
    '''Class to custom Exception'''
    def __init__(self, message, estado='', step=''):
        self.message = message
        self.estado = estado
        self.step =  step

        super().__init__(self.message, self.estado, self.step)
