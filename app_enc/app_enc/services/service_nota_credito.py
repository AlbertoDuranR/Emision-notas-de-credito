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

    def crear_nota_credito(sol_id):
        # print('data_solicitud', sol_id)
        '''
            # obtener de Postgres:
            ## view : view_solicitudes_nota_de_credito
            - sn.sol_id,
            - sn.sol_fecha_solicitud,
            - sn.sol_tipo_nc, <- PDV | Fin | Ser
            - sn.sol_estado,
            - ds.det_nro_comprobante, <- Origen documento
            - ds.det_metodo, <- Total o Parcial Solo para PDV
            - ds.det_monto_total_prod <- Monto de solicitud
            ## Productos
            - dpro_codigo
            - dpro_cantidad
            # Obtener de Dynamics
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

        data_solicitud = {
            # Datos para RPA
            'num_comprobante_origen': det_nro_comprobante,
            'num_pedido_origen': num_pedido_origen,
            'metodo': det_metodo,
            'almacen': cod_almacen,
            'productos': list_productos,
            'forma_pago': cod_forma_pago,
            'pago': temino_pago,
            'fecha_solicitud': sol_fecha_solicitud.strftime("%m/%d/%Y"), # 1/21/2024
            'monto_total_nota_credito': det_monto_total_prod # Parcial: Monto del producto | Total: Monto total de comprobante
        }

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

        if sol_tipo_nc == 'PDV' and sol_estado == 'VALIDADO':
            print('Data_solicitud: ', data_solicitud)
            dynamics_bot = Dynamics_Bot()
            dynamics_bot.iniciar_sesion()
            dynamics_bot.crear_nota_de_credito(data=data_solicitud)
