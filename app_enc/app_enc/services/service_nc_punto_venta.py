from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime

## Models
from ..models.model_solicitud_nc import SolicitudNC
from ..models.model_producto_detalle import ProductoDetalle
from ..models.model_detalle_solicitud import DetalleSolicitud

class ServiceNCPDV:
    # vista
    def lista_solicitudes():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM consolidado_pdv")
            results = cursor.fetchall()
        lista_diccionarios = []
        for tupla in results:
            #print(tupla)
            nro_nota_credito = tupla[14]
            nro_pedido_nota_credito = tupla[15]
            estado_nota_credito = 'PENDIENTE'
            if nro_pedido_nota_credito:
                if nro_nota_credito:
                    estado_nota_credito = 'CREADO'
                else:
                    estado_nota_credito = 'ERROR'

            diccionario = {
                'ID_NC': tupla[0],
                'ID_DETALLE': tupla[1],
                'FECHA_SOLICITUD': tupla[2],
                'USUARIO_CREADOR': tupla[3],
                'ESTABLECIMIENTO': tupla[4],
                'FECHA_EMISION': tupla[5],
                'TIPO': tupla[6],
                'NRO_COMPROBANTE': tupla[7],
                'ESTADO': tupla[8],
                'FECHA_CREACION': tupla[9],
                'METODO': tupla[10],
                'MONTO_TOTAL': tupla[11],
                'ACEPTA': tupla[12],
                'OBSERVACION': tupla[13],
                'NRO_NOTA_CREDITO': nro_nota_credito,
                'NRO_PEDIDO_NOTA_CREDITO': nro_pedido_nota_credito,
                'ESTADO_NOTA_CREDITO': estado_nota_credito,
                'OBS_ESTADO_RPA_NOTA_CREDITO': estado_nota_credito == 'ERROR' if tupla[13] else '',
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios
    
    def lista_solicitudesEdit(id):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM public.listar_solicitud_pdv({id})")
            results = cursor.fetchall()
        print('lista_solicitudeEdit', results)
        lista_diccionarios = []
        for tupla in results:
            #print(tupla)
            diccionario = {
                'ID_NC': tupla[0],
                'ID_DETALLE': tupla[1],
                'FECHA_EMISION': tupla[2],
                'NUMERO_COMPROBANTE': tupla[3],
                'IMPORTE_TOTAL': tupla[4],
                'FECHA_SOLICITUD': tupla[5],
                'MOTIVO': tupla[6],
                'JUSTIFICACION': tupla[7],
                'METODO': tupla[8],
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios
    
    def lista_productosEdit(id):
        with connection.cursor() as cursor:
            cursor.execute(f"select dpro_codigo, dpro_descripcion,dpro_unidad,dpro_precio,dpro_cantidad,dpro_monto_total from public.producto_detalle where det_id = {id}")
            results = cursor.fetchall()
        lista_diccionarios = []
        for tupla in results:
            #print(tupla)
            diccionario = {
                'PRODUCTO_CODIGO': tupla[0],
                'PRODUCTO_DESCRIPCION': tupla[1],
                'PRODUCTO_UNIDAD': tupla[2],
                'PRODUCTO_PRECIO': tupla[3],
                'PRODUCTO_CANTIDAD': tupla[4],
                'PRODUCTO_MONTO': tupla[5]
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios

    def save_solicitud(data):
        # Solicitud NC
        tipo_nc = "PDV"
        usuario_creador = 1 # Sera el Id del Usuario
        estado = "PENDIENTE"
        fecha_emision = data["datos_documento"]["fecha_emision"]['date']
        fecha_emision = datetime.strptime(fecha_emision,'%Y-%m-%dT%H:%M:%S.%fZ')
        # Detalle
        fecha_solicitud = data["detalle_solicitud"]["fecha_solicitud"]['date']
        fecha_solicitud = datetime.strptime(fecha_solicitud,'%Y-%m-%dT%H:%M:%S.%fZ')
        nro_comprobante = data["datos_documento"]["nro_comprobante"]
        motivo = data["detalle_solicitud"]["motivo"]
        importe_total = float(data["datos_documento"]["importe_total"])
        justificacion = data["detalle_solicitud"]["justificacion"]
        metodo = data["detalle_solicitud"]["metodo"]
        # Productos
        metodo_parcial_productos=data["metodo_parcial_productos"]
        monto_total_productos=importe_total

        if not motivo or not justificacion:
            raise TypeError("Motivo y Jutificación son necesarios")

        if metodo=="parcial":
            if metodo_parcial_productos:
                monto_total_productos = round(sum(float(producto["Total"]) for producto in metodo_parcial_productos), 2)
                importe_total = monto_total_productos
            else:
                raise TypeError("Metodo Parcial no tiene productos")

        # Guardar Solicitud de Nota de Crédito
        solicitud_nc = SolicitudNC(
            sol_fecha_solicitud=fecha_solicitud.date(),
            sol_tipo_nc=tipo_nc,
            sol_usuario_creador=usuario_creador,
            sol_fecha_creacion=datetime.now().date(),
            sol_estado=estado
        )
        solicitud_nc.save()

        # Guardar Detalle de la Solicitud de Nota de Crédito
        detalle = DetalleSolicitud(
            det_fecha_emision=fecha_emision.date(),
            det_nro_comprobante=nro_comprobante,
            det_importe_total=importe_total,
            det_motivo=motivo,
            det_justificacion=justificacion,
            det_metodo=metodo,
            det_monto_total_prod=monto_total_productos,
            det_establecimiento=1, ## Lugar de solicitud
            sol_id=solicitud_nc.sol_id
        )
        detalle.save()

        # Guardar Productos de la Solicitud si es parcial
        if metodo=="parcial" and metodo_parcial_productos:
            print("Si contiene productos")
            producto_detalle = []
            for producto in metodo_parcial_productos:
                producto_detalle.append(ProductoDetalle(
                    dpro_codigo=producto["ProductNumber"],
                    dpro_descripcion=producto["ProductDescription"],
                    dpro_unidad=producto["SalesUnitSymbol"],
                    dpro_precio=float(producto["SalesPrice"]),
                    dpro_cantidad=int(producto["InvoicedQuantity"]),
                    dpro_monto_total= float(producto["Total"]),
                    det_id=detalle.det_id
                ))
            ProductoDetalle.objects.bulk_create(producto_detalle)

    def save_observacion(data):
        sol_id = int(data["id"])
        observacion = data["observacion"]
        estado = "OBSERVADO"
        solicitud_existente = SolicitudNC.objects.filter(sol_id=sol_id).first()
        if solicitud_existente:
            # Actualizar el registro existente en SolicitudNC
            solicitud_existente.sol_observacion = observacion
            solicitud_existente.sol_estado = estado
            solicitud_existente.save()

    # Actualizar solicitud - puntos de venta
    def edit_solicitud(data):
        sol_id = int(data["datos_documento"]["id_nc"])
        det_id = int(data["datos_documento"]["id_detalle_nc"])

        # Solicitud NC
        tipo_nc = "PDV"
        usuario_creador = 1 ##
        estado = "ACTUALIZADO"
        fecha_emision = data["datos_documento"]["fecha_emsion"]['date']
        fecha_emision = datetime.strptime(fecha_emision, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Detalle
        fecha_solicitud = data["detalle_solicitud"]["fecha_solicitud"]['date']
        fecha_solicitud = datetime.strptime(fecha_solicitud, '%Y-%m-%dT%H:%M:%S.%fZ')
        nro_comprobante = data["datos_documento"]["nro_comprobante"]
        motivo = data["detalle_solicitud"]["motivo"]
        importe_total = data["datos_documento"]["importe_total"]
        justificacion = data["detalle_solicitud"]["justificacion"]
        metodo = data["detalle_solicitud"]["metodo"]
        # Producto
        metodo_parcial_productos=data["metodo_parcial_productos"]
        monto_total_productos=importe_total

        if not motivo or not justificacion:
            raise TypeError("Motivo y Jutificación son necesarios")

        if metodo=="parcial":
            if metodo_parcial_productos:
                monto_total_productos = round(sum(float(producto["Total"]) for producto in metodo_parcial_productos), 2)
            else:
                raise TypeError("Metodo Parcial no tiene productos")

        # 1. eliminarmos productos
        productos_eliminados = ProductoDetalle.objects.filter(det_id=det_id) # Verificar det_id ??
        if productos_eliminados:
            productos_eliminados.delete()

        # 2. ACTUALIZAMOS solicitud_nc
        solicitud_existente = SolicitudNC.objects.filter(sol_id=sol_id).first()
        if solicitud_existente:
            # Actualizar el registro existente en SolicitudNC
            solicitud_existente.sol_fecha_solicitud = fecha_solicitud.date()
            solicitud_existente.sol_tipo_nc = tipo_nc
            solicitud_existente.sol_usuario_creador = usuario_creador
            solicitud_existente.sol_fecha_creacion = datetime.now().date()
            solicitud_existente.sol_fecha_modificacion = datetime.now().date()
            solicitud_existente.sol_estado = estado
            solicitud_existente.save()

        # 3. actualizamos detalle_solicitud
        detalle_existente = DetalleSolicitud.objects.filter(det_id=det_id).first()
        if detalle_existente:
            # Actualizar DetalleSolicitud
            detalle_existente.det_fecha_emision = fecha_emision.date()
            detalle_existente.det_nro_comprobante = nro_comprobante
            detalle_existente.det_importe_total = importe_total
            detalle_existente.det_motivo = motivo
            detalle_existente.det_justificacion = justificacion
            detalle_existente.det_metodo = metodo
            detalle_existente.det_monto_total_prod = monto_total_productos
            detalle_existente.det_establecimiento = 1
            detalle_existente.save()

         # 4. creamos los nuevos productos
        if metodo=="parcial" and metodo_parcial_productos:
            print("Si contiene productos")
            producto_detalle = []
            for producto in metodo_parcial_productos:
                producto_detalle.append(ProductoDetalle(
                    dpro_codigo=producto["ProductNumber"],
                    dpro_descripcion=producto["ProductDescription"],
                    dpro_unidad=producto["SalesUnitSymbol"],
                    dpro_precio=float(producto["SalesPrice"]),
                    dpro_cantidad=int(producto["InvoicedQuantity"]),
                    dpro_monto_total= float(producto["Total"]),
                    det_id=detalle_existente.det_id
                ))
            ProductoDetalle.objects.bulk_create(producto_detalle)

    def delete_solicitud(id):
        estado = 'ELIMINADO'
        
        solicitud_existente = SolicitudNC.objects.filter(sol_id=id).first()
        if solicitud_existente:
            solicitud_existente.sol_estado = estado
            solicitud_existente.save()     

    def validate_solicitud(data):
        id = data['id']
        estado = 'VALIDADO'
        solicitud_existente = SolicitudNC.objects.filter(sol_id=id).first()
        if solicitud_existente:
            solicitud_existente.sol_estado = estado
            solicitud_existente.sol_fecha_modificacion = datetime.now().date()
            solicitud_existente.save()

    def getDataCorreo():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM listar_consolidado_pdv()")
            results = cursor.fetchall()
        lista_diccionarios = []
        for tupla in results:
            #print(tupla)
            diccionario = {
                'ID_NC': tupla[0],
                'ID_DETALLE': tupla[1],
                'CREADOR_USUARIO': tupla[2],
                'TIPO_COMPROBANTE': tupla[3],
                'FECHA_CREAR_NC': tupla[4],
                'ESTADO': tupla[5],
                'EMISION_COMPROBANTE': tupla[6],
                'NRO': tupla[7],
                'IMPORTE': tupla[8],
                'IMPORTE_PRODUCTOS': tupla[9],
                'METODO': tupla[10]
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios