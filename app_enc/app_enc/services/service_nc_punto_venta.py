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

    # huardar solicitud - púntos de venta
    def save_solicitud(data):
        # Solicitud NC
        tipo_nc = "PDV"
        usuario_creador = 1 ##
        estado = "EMITIDO"
        fecha_emision = data["datos_documento"]["fecha_emsion"]['date']
        fecha_emision = datetime.strptime(fecha_emision,'%Y-%m-%dT%H:%M:%S.%fZ')
        # Detalle 
        fecha_solicitud = data["detalle_solicitud"]["fecha_solicitud"]['date']
        fecha_solicitud = datetime.strptime(fecha_solicitud,'%Y-%m-%dT%H:%M:%S.%fZ')
        nro_comprobante = data["datos_documento"]["nro_comprobante"]
        motivo = data["detalle_solicitud"]["motivo"]
        importe_total = data["datos_documento"]["importe_total"]
        justificacion = data["detalle_solicitud"]["justificacion"]
        metodo = data["detalle_solicitud"]["metodo"]
        # Producto
        codigo_descripcion = data["metodo_parcial_productos"]["value"]
        cont_productos=False
        if codigo_descripcion is not None and metodo=="Parcial":
            if len(codigo_descripcion) != 0:
                monto_producto = data["metodo_parcial_productos"]["monto_total"]["valores"][0:len(codigo_descripcion)]
                ##
                monto_total_productos = 0
                for x in monto_producto:
                    monto_total_productos = monto_total_productos + int(x["value"])
                
                cont_productos=True
                print(monto_total_productos)
            else:
                raise TypeError("Campo necesario vacio.")
        elif metodo == "Parcial" and codigo_descripcion is None:
            raise TypeError("Campo necesario vacio.")
        
        #print(fecha_emision.date())
        # Guardando
        solicitud_nc = SolicitudNC(
            sol_fecha_solicitud=fecha_solicitud.date(),
            sol_tipo_nc=tipo_nc,
            sol_usuario_creador=usuario_creador,
            sol_fecha_creacion=datetime.now().date(),
            sol_estado=estado
        )
        solicitud_nc.save()
        #
        if cont_productos: #Si contiene productos
            detalle = DetalleSolicitud(
                det_fecha_emision=fecha_emision.date(),
                det_nro_comprobante=nro_comprobante,
                det_importe_total=importe_total,
                det_motivo=motivo,
                det_justificacion=justificacion,
                det_metodo=metodo,
                det_monto_total_prod=monto_total_productos,
                det_establecimiento=1, ##
                sol_id=solicitud_nc.sol_id
            )
            detalle.save()
            ##
            unidades = data["metodo_parcial_productos"]["unidad"]["valores"][0:len(codigo_descripcion)]
            precios = data["metodo_parcial_productos"]["precio"]["valores"][0:len(codigo_descripcion)]
            cantidades = data["metodo_parcial_productos"]["cantidad"]["valores"][0:len(codigo_descripcion)]
            monto_producto = data["metodo_parcial_productos"]["monto_total"]["valores"][0:len(codigo_descripcion)]
            producto_detalle = []
            for x in range(len(codigo_descripcion)):
                #codigo
                producto_detalle.append(ProductoDetalle(
                    dpro_codigo=codigo_descripcion[x]["ProductNumber"],
                    dpro_descripcion=codigo_descripcion[x]["ProductDescription"],
                    dpro_unidad=unidades[x]["value"]["UnitSymbol"],
                    dpro_precio=float(precios[x]["value"]),
                    dpro_cantidad=int(cantidades[x]["value"]),
                    dpro_monto_total= float(monto_producto[x]["value"]),
                    det_id=detalle.det_id
                ))
            ##
            # print("aquiiii")
            # print(producto_detalle)
            ProductoDetalle.objects.bulk_create(producto_detalle)
        else: #No contiene productos
            detalle = DetalleSolicitud(
                det_fecha_emision=fecha_solicitud.date(),
                det_nro_comprobante=nro_comprobante,
                det_importe_total=importe_total,
                det_motivo=motivo,
                det_justificacion=justificacion,
                det_metodo=metodo,
                det_monto_total_prod=importe_total,
                det_establecimiento=1, ##
                sol_id=solicitud_nc.sol_id
            )
            detalle.save()
    
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