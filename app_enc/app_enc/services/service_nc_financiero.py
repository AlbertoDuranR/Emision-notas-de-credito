from django.shortcuts import render, redirect
from ..models.model_solicitud_nc import SolicitudNC
from ..models.model_detalle_solicitud import DetalleSolicitud
from ..models.model_solicitante_detalle import SolicitanteDet
from ..models.model_market import Market
from datetime import datetime
from django.db import connection

class ServiceNCFinanciero:

    def show_solicitud(request):
        solicitud = SolicitudNC.objects.all()
        print("aqui",solicitud)
    
    def get_all_markets():
        return list(Market.objects.all())
    
    def lista_solicitudes():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM listar_consolidado_fin()")
            results = cursor.fetchall()
        lista_diccionarios = []
        for tupla in results:
            #print(tupla)
            diccionario = {
                'ID_NC': tupla[0],
                'ID_DETALLE': tupla[1],
                'ESTABLECIMIENTO': tupla[2],
                'ESTADO': tupla[3],
                'EMISION_COMPROBANTE': tupla[4],
                'NRO': tupla[5],
                'IMPORTE': tupla[6],
                'DESCUENTO': tupla[7],
                'TOTAL_DESCUENTO': tupla[8],
                'BOLETEO': tupla[9],
                'FECHA_SOLICITUD': tupla[10],
                'SOLICITANTE': tupla[11],
                'LABORA_EN': tupla[12]
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios

    def save_solicitud(data):
        # Solicitud NC
        tipo_nc = "FIN"
        usuario_creador = 1 ##
        estado = "EMITIDO"
        fecha_solicitud = data["detalle_solicitante"]["fecha_solicitud"]['date']
        fecha_solicitud = datetime.strptime(fecha_solicitud,'%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Detalle 
        fecha_emision = data["datos_documento"]["fecha_emision"]['date']
        fecha_emision = datetime.strptime(fecha_emision,'%Y-%m-%dT%H:%M:%S.%fZ')
        nro_comprobante = data["datos_documento"]["nro_comprobante"]
        importe_c = data["datos_documento"]["importe_real"]
        descuento = data["datos_documento"]["descuento"]
        total_descuento = data["datos_documento"]["total_descuento"]
        boleteo = data["datos_documento"]["boleteo"]
        d_establecimiento=data["datos_documento"]["establecimiento"]["value"]["mar_id"]
        
        #Solicitante
        dni = data["detalle_solicitante"]["dni"]
        ap_materno = data["detalle_solicitante"]["ap_materno"]
        ap_paterno = data["detalle_solicitante"]["ap_paterno"]
        nombre = data["detalle_solicitante"]["nombres"]
        labora_en= data["detalle_solicitante"]["lugar_donde_labora"]["value"]["mar_id"]

        ## Guardando
        solicitud_nc = SolicitudNC(
            sol_fecha_solicitud=fecha_solicitud.date(),
            sol_tipo_nc=tipo_nc,
            sol_usuario_creador=usuario_creador,
            sol_fecha_creacion=datetime.now().date(),
            sol_estado=estado
        )
        solicitud_nc.save()

        ##
        solicitante = SolicitanteDet(
            sdet_dni=dni,
            sdet_materno=ap_materno,
            sdet_paterno=ap_paterno,
            sdet_nombres=nombre
        )
        ##
        solicitante.save()
        #
        detalle_sol = DetalleSolicitud(
            det_fecha_emision=fecha_emision.date(),
            det_nro_comprobante=nro_comprobante,
            det_importe_total=importe_c,
            det_establecimiento=int(d_establecimiento),
            det_descuento=descuento,
            det_total_descuento=total_descuento,
            det_boleteo=boleteo,
            sdet_id=solicitante.sdet_id,
            det_labora_en=int(labora_en),
            sol_id=solicitud_nc.sol_id
        )
        detalle_sol.save()