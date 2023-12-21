from django.shortcuts import render, redirect
from ..models.model_solicitud_nc import SolicitudNC
from ..models.model_detalle_solicitud import DetalleSolicitud
from ..models.model_solicitante_detalle import SolicitanteDet
from ..models.model_market import Market
from datetime import datetime
from django.db import connection
import requests

class ServiceNCFinanciero:

    def show_solicitud(request):
        solicitud = SolicitudNC.objects.all()
        print("aqui",solicitud)
    
    def get_all_markets():
        return list(Market.objects.all())
    
    def lista_solicitudes():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM consolidado_financiero")
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
                'TIPO_COMPROBANTE': tupla[5],
                'NUMERO_COMPROBANTE': tupla[6],
                'DESCUENTO': tupla[7],
                'TOTAL_DESCUENTO': tupla[8],
                'ESTADO': tupla[9],
                'FECHA_CREACION': tupla[10],
                'IMPORTE_TOTAL': tupla[11],
                'ACEPTA': tupla[12],
                'OBSERVACION': tupla[13],
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios
    
    def lista_solicitudesEdit(id):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM public.listar_solicitud_fin({id})")
            results = cursor.fetchall()
        lista_diccionarios = []
        for tupla in results:
            #print(tupla)
            diccionario = {
               'ID_NC': tupla[0],
               'ID_DETALLE': tupla[1],
               'ID_DETALLE_SOLICITANTE': tupla[2],
               'ID_ESTABLECIMIENTO': tupla[3],
               'FECHA_EMISION': tupla[4],
               'NRO_COMPROBANTE': tupla[5],
               'IMPORTE_REAL': tupla[6],
               'DESCUENTO': tupla[7],
               'TOTAL_DESCUENTO': tupla[8],
               'BOLETEO': tupla[9],
               'FECHA_SOLICITUD': tupla[10],
               'DNI': tupla[11],
               'APELLIDO_MATERNO': tupla[12],
               'APELLIDO_PATERNO': tupla[13],
               'NOMBRES': tupla[14],
               'ID_MARKET': tupla[15]
            }
            lista_diccionarios.append(diccionario)
        return lista_diccionarios

    def save_solicitud(data):
        # Solicitud NC
        tipo_nc = "FIN"
        usuario_creador = 1 ##
        estado = "PENDIENTE"
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
        sol_id = int(data["datos_documento"]["id_nc"])
        det_id = int(data["datos_documento"]["id_detalle_nc"])
        sdet_id = int(data["datos_documento"]["id_detalle_cliente"])
        
         # Solicitud NC
        tipo_nc = "FIN"
        usuario_creador = 1 ##
        estado = "ACTUALIZADO"
        
        # Datos de Documento Solicitud
        #Establecimiento
        Establecimiento = data["datos_documento"]["establecimiento"]["value"]["mar_id"]
        # Fecha emisión del comprobantes:
        fecha_emision = data["datos_documento"]["fecha_emision"]['date']
        fecha_emision = datetime.strptime(fecha_emision,'%Y-%m-%dT%H:%M:%S.%fZ')
        # Nro. Comprobante:
        nro_comprobante = data["datos_documento"]["nro_comprobante"]
        # Importe Real
        importe_real = data["datos_documento"]["importe_real"]
        # Descuento 
        descuento = data["datos_documento"]["descuento"]
        # Total Descuento:
        total_descuento = data["datos_documento"]["total_descuento"]
        # Boleteo
        boleteo = data["datos_documento"]["boleteo"]
        
        ## Detalle de Solicitante
        # Fecha emisión de la nota de crédito:
        fecha_solicitud = data["detalle_solicitante"]["fecha_solicitud"]['date']
        fecha_solicitud = datetime.strptime(fecha_solicitud,'%Y-%m-%dT%H:%M:%S.%fZ')
        # DNI
        dni = data["detalle_solicitante"]["dni"]
        # Apellido Materno
        ap_materno = data["detalle_solicitante"]["ap_materno"]
        # Apellido Paterno
        ap_paterno = data["detalle_solicitante"]["ap_paterno"]
        # Nombres
        nombres = data["detalle_solicitante"]["nombres"]
        # Lugar donde labora:
        lugar_donde_labora = data["detalle_solicitante"]["lugar_donde_labora"]["value"]["mar_id"]
        
        
        detalle_solicitante_solicitud = SolicitanteDet.objects.filter(sdet_id=sdet_id).first()        
        #  Verificar si ya existe un registro en SolicitudNC
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
                detalle_existente.det_fecha_emision = fecha_emision.date()
                detalle_existente.det_nro_comprobante = nro_comprobante
                detalle_existente.det_importe_total = importe_real
                detalle_existente.det_establecimiento = int(Establecimiento)
                detalle_existente.det_descuento = int(descuento)
                detalle_existente.det_total_descuento = total_descuento
                detalle_existente.det_boleteo = boleteo
                detalle_existente.save()
                
                detalle_solicitante_solicitud = SolicitanteDet.objects.filter(sdet_id=sdet_id).first()
                
                if detalle_solicitante_solicitud:
                    print(int(sdet_id))
                    
                    detalle_solicitante_solicitud.sdet_dni = dni
                    detalle_solicitante_solicitud.sdet_materno = ap_materno
                    detalle_solicitante_solicitud.sdet_paterno = ap_paterno
                    detalle_solicitante_solicitud.sdet_nombres = nombres
                    detalle_solicitante_solicitud.save()
               
            
                    
    def delete_solicitud(id):
            estado = 'ELIMINADO'
            
            solicitud_existente = SolicitudNC.objects.filter(sol_id=id).first()
            if solicitud_existente:
                solicitud_existente.sol_estado = estado
                solicitud_existente.save()                  
                
    def validate_solicitud(data):
        id = data['id']
        estado = data['estado']
        
        solicitud_existente = SolicitudNC.objects.filter(sol_id=id).first()
        if solicitud_existente:
            solicitud_existente.sol_estado = estado
            solicitud_existente.sol_fecha_modificacion = datetime.now().date()
            solicitud_existente.save()
            
    def fetch_reniec_data(data):
        
       
        dni = data["dni"]
        base_url = "https://api.dniruc.com/api/search/dni/"
        api_key = "Live_c386df4ae4f0f64f4c5ab574e5a71a59f22e08b6"  # Reemplaza con tu clave API

        url = f"{base_url}{dni}/{api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            
            #print(data)
            return data["data"]

        except requests.exceptions.RequestException as error:
            print(f"Error en la solicitud: {error}")
            return None  # Puedes manejar el error de otra manera si es necesario
                    