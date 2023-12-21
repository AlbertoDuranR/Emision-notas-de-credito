from datetime import datetime
from ..models.model_solicitud_nc import SolicitudNC
from ..models.model_detalle_solicitud import DetalleSolicitud
from django.db import connection

class ServiceNCServicios:

    def lista_solicitudes():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM consolidado_servicios")
            results = cursor.fetchall()
        lista_diccionarios = []
        for tupla in results:
            #print(tupla)
            diccionario = {
                'ID_NC': tupla[0],
                'FECHA_SOLICITUD': tupla[1],
                'USUARIO_CREADOR': tupla[2],
                'ESTABLECIMIENTO': tupla[3],
                'FECHA_EMISION': tupla[4],
                'TIPO': tupla[5],
                'COMPROBANTE': tupla[6],
                'ESTADO':tupla[7],
                'FECHA_CREACION':tupla[8],
                'IMPORTE_TOTAL':tupla[9],
                'ACEPTA':tupla[10],
                'OBSERVACION': tupla[11],
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios
    
    def lista_solicitudesEdit(id):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM public.listar_solicitud_ser({id})")
            results = cursor.fetchall()
        lista_diccionarios = []
        for tupla in results:
            diccionario = {
                'ID_NC': tupla[0],
                'ID_DETALLE_NC': tupla[1],
                'FECHA_EMISION': tupla[2],
                'NRO_COMPROBANTE': tupla[3],
                'MOTIVO': tupla[4],
                'IMPORTE_TOTAL': tupla[5],
                'FECHA_SOLICITUD': tupla[6],
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios

    def save_solicitud(data):
        # Solicitud NC
        tipo_nc = "SER"
        usuario_creador=1 ##
        estado = "EMITIDO"
        fecha_solicitud = data["datos_documento"]["fecha_emision_nc"]['date']
        fecha_solicitud = datetime.strptime(fecha_solicitud,'%Y-%m-%dT%H:%M:%S.%fZ')

        # Detalle
        fecha_emision = data["datos_documento"]["fecha_emision"]['date']
        fecha_emision = datetime.strptime(fecha_emision,'%Y-%m-%dT%H:%M:%S.%fZ')
        nro_comprobante= data["datos_documento"]["nro_comprobante"]
        motivo= data["datos_documento"]["motivo"]
        importe_total= data["datos_documento"]["importe_nc"]

        ## Guardando
        solicitud_nc = SolicitudNC(
            sol_fecha_solicitud=fecha_solicitud.date(),
            sol_tipo_nc=tipo_nc,
            sol_usuario_creador=usuario_creador,
            sol_fecha_creacion=datetime.now().date(),
            sol_estado=estado
        )
        solicitud_nc.save()
        #
        detalle_sol = DetalleSolicitud(
            det_fecha_emision=fecha_emision.date(),
            det_nro_comprobante=nro_comprobante,
            det_importe_total=importe_total,
            det_motivo=motivo,
            sol_id=solicitud_nc.sol_id
        )
        detalle_sol.save()

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
        
    def edit_solicitud(data):
        # Solicitud NC
        sol_id = data["datos_documento"]["id_nc"]
        det_id = data["datos_documento"]["id_detalle_nc"]
        
        tipo_nc = "SER"
        usuario_creador = 1
        estado = "ACTUALIZADO"
        fecha_solicitud = data["datos_documento"]["fecha_emision_nc"]['date']
        fecha_solicitud = datetime.strptime(fecha_solicitud, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Detalle
        fecha_emision = data["datos_documento"]["fecha_emision"]['date']
        fecha_emision = datetime.strptime(fecha_emision, '%Y-%m-%dT%H:%M:%S.%fZ')
        nro_comprobante = data["datos_documento"]["nro_comprobante"]
        motivo = data["datos_documento"]["motivo"]
        importe_total = data["datos_documento"]["importe_nc"]
        
        # Imprimir todos los datos
        # print("sol_id:", sol_id)
        # print("det_id:", det_id)
        # print("tipo_nc:", tipo_nc)
        # print("usuario_creador:", usuario_creador)
        # print("estado:", estado)
        # print("fecha_solicitud:", fecha_solicitud)
        # print("fecha_emision:", fecha_emision)
        # print("nro_comprobante:", nro_comprobante)
        # print("motivo:", motivo)
        # print("importe_total:", importe_total)

        # Verificar si ya existe un registro en SolicitudNC
        solicitud_existente = SolicitudNC.objects.filter(sol_id=sol_id).first()

        if solicitud_existente:
            # Actualizar el registro existente en SolicitudNC
            solicitud_existente.sol_fecha_solicitud = fecha_solicitud.date()
            solicitud_existente.sol_tipo_nc = tipo_nc
            solicitud_existente.sol_usuario_creador = usuario_creador
            solicitud_existente.sol_fecha_creacion = datetime.now().date()
            solicitud_existente.sol_estado = estado
            solicitud_existente.save()

            # Verificar si ya existe un registro en DetalleSolicitud
            detalle_existente = DetalleSolicitud.objects.filter(det_id=det_id).first()

            if detalle_existente:
                # Actualizar DetalleSolicitud
                detalle_existente.det_fecha_emision = fecha_emision.date()
                detalle_existente.det_nro_comprobante = nro_comprobante
                detalle_existente.det_importe_total = importe_total
                detalle_existente.det_motivo = motivo
                detalle_existente.save()

    def delete_solicitud(id):
            estado = 'ELIMINADO'
            
            solicitud_existente = SolicitudNC.objects.filter(sol_id=id).first()
            if solicitud_existente:
                solicitud_existente.sol_estado = estado
                solicitud_existente.save()  

    def validate_solicitud(data):
        print(data)
        
        id = data['id']
        estado = data['estado']
        
        solicitud_existente = SolicitudNC.objects.filter(sol_id=id).first()
        if solicitud_existente:
            solicitud_existente.sol_estado = estado
            solicitud_existente.sol_fecha_modificacion = datetime.now().date()
            solicitud_existente.save() 