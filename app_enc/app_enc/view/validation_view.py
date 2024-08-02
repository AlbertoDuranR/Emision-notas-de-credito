import json
import logging
from django.http import JsonResponse
from django.middleware.csrf import get_token
from ..services.service_nc_punto_venta import ServiceNCPDV
from ..services.service_dynamics import ServiceDynamics
from ..scrapers.acepta_page_bot.acepta_page_bot import AceptaScraper
from ..models.model_view_solicitudes_nota_de_credito import ViewSolicitudNotaDeCredito


servicePDV = ServiceNCPDV
serviceDynamics = ServiceDynamics()

# Obtener el logger para el módulo actual (o elige un nombre específico)
logger = logging.getLogger(__name__)


class ValidationView:

    def validar_comprobante(request):
        if request.method == "POST":
            # Transform data
            data = json.loads(request.body.decode('utf-8'))
            nro_comprobante = data['nro_comprobante'] # 'BG02-00052743'
            sales_invoice = serviceDynamics.get_sales_invoice_headers_by_invoice_number(nro_comprobante)
            if not sales_invoice:
                data["observacion"] = "Comprobante de origen no se encontro en Dynamics365. Verificar Nro de Comprobante"
                servicePDV.save_observacion(data)
                logger.warning(f'Estado Dynamics 365: {data}')
                return JsonResponse({'message': 'Comprobante de origen no se encontro en Dynamics365'}, status=404)
            # logger.info(f'Estado Dynamics 365: {sales_invoice}')

            aceptaScraper = AceptaScraper() # Creamos un Objeto - instancia
            estado_acepta = aceptaScraper.get_estado_por_comprobante(nro_comprobante)
            estado_comprobante = estado_acepta['estado']
            error_comprobante = estado_acepta['error']
            # print('estado_acepta'*5, estado_acepta)
            if estado_comprobante is None:
                obs = f'Error al obtener el estado en el Portal ACEPTA. {error_comprobante}'
                logger.warning(obs)
                data["observacion"] = obs
                servicePDV.save_observacion(data)
                return JsonResponse({'message': obs}, status=500)

            if not estado_comprobante == 'ACEPTADO':
                logger.warning(f'Estado Portal Acepta: {estado_comprobante}')
                obs = f'Comprobante no se encuentra ACEPTADO en el PORTAL ACEPTA. Estado: {estado_comprobante}'
                data["observacion"] = obs
                servicePDV.save_observacion(data)
                return JsonResponse({'message': obs}, status=404)

            logger.info(f'Estado Dynamics 365: {estado_comprobante}')

            try:
                servicePDV.validate_solicitud(data)
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print(e)
                logger.error(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)

    def validar_comprobantes(request):
        if request.method == "POST":
            comprobantes = [] # [{'id': 1, 'nro_comprobante': 'BG02-00052743', 'estado': 'ACEPTADO', 'observacion': ''},]
            solicitudes = ViewSolicitudNotaDeCredito.objects.filter(sol_estado='PENDIENTE', sol_tipo_nc='PDV') # Buscar todas las solicitudes con estado PENDIENTE
            if not solicitudes:
                return JsonResponse({'message': 'No se encontraron Solicitudes PENDIENTES'}, status=404)
            for solicitud in solicitudes:
                comprobantes.append({'id': solicitud.sol_id, 'nro_comprobante' : solicitud.det_nro_comprobante, 'estado': solicitud.sol_estado})

            _comprobantes = ValidationView._validar_en_dynamic(comprobantes=comprobantes)
            _comprobantes = ValidationView._validar_en_acepta(comprobantes=_comprobantes, tipo='COMPROBANTE')
            try:
                comprobantes_validados = [comprobante for comprobante in _comprobantes if comprobante['estado'] == 'ACEPTADO']
                for comprobante_validar in comprobantes_validados:
                    servicePDV.validate_solicitud(comprobante_validar)
                return JsonResponse({'message': f'Datos procesados correctamente: Se validaron {len(comprobantes_validados)} / {len(comprobantes)}'}, status=200)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)

    def validar_notas(request):
        if request.method == "POST":
            notas = [] # [{'id': 1, 'nro_comprobante': 'BG02-00052743', 'estado': 'ACEPTADO', 'observacion': ''},]
            solicitudes = ViewSolicitudNotaDeCredito.objects.filter(sol_estado='CREADO',det_nro_nota_credito__isnull=False).exclude(sol_acepta='ACEPTADO') # Solicitudes que tiene notas de credito
            if not solicitudes:
                return JsonResponse({'message': 'No se encontraron Solicitudes CREADAS con Notas de Crédito'}, status=404)
            for solicitud in solicitudes:
                notas.append({'id': solicitud.sol_id, 'nro_comprobante' : solicitud.det_nro_nota_credito, 'estado': solicitud.sol_acepta})

            _notas = ValidationView._validar_en_acepta(comprobantes=notas, tipo='NOTAS')
            try:
                notas_validadas = [nota for nota in _notas if nota['estado'] == 'ACEPTADO']
                for nota_validar in notas_validadas:
                    servicePDV.validate_nota(nota_validar)
                return JsonResponse({'message': f'Datos procesados correctamente: Se validaron {len(notas_validadas)} / {len(notas)}'}, status=200)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'message': 'Error al procesar los datos'}, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)

    def _validar_en_dynamic(comprobantes):
        print('Validar en dynamics')
        _comprobantes = comprobantes
        for comprobante in _comprobantes:
            sales_invoice = serviceDynamics.get_sales_invoice_headers_by_invoice_number(comprobante['nro_comprobante'])
            if not sales_invoice:
                comprobante["observacion"] = "Comprobante de origen no se encontro en Dynamics365. Verificar Nro de Comprobante"
                servicePDV.save_observacion(comprobante)
                logger.warning(f'Estado Dynamics 365: {comprobante}')
                # logger.warning(f'Estado Dynamics 365: Existe')
            comprobante["estado"] = 'ENCONTRADO'
        return _comprobantes

    def _validar_en_acepta(comprobantes, tipo: str):
            print('Validar en Acepta', comprobantes)
            _comprobantes = comprobantes
            nros_comprobantes = [comprobante['nro_comprobante'] for comprobante in _comprobantes]
            aceptaScraper = AceptaScraper() # Creamos un Objeto - instancia
            estados_acepta = aceptaScraper.get_estados_de_comprobantes(nros_comprobantes)
            for comprobante in _comprobantes:
                estado_acepta = estados_acepta[comprobante['nro_comprobante']]
                estado_comprobante = estado_acepta['estado']
                error_comprobante = estado_acepta['error']

                if estado_comprobante is None:
                    comprobante["observacion"] = f'Error al obtener el estado en el Portal ACEPTA: {error_comprobante}'
                    if tipo == 'NOTAS':
                            servicePDV.save_observacion_nota(comprobante['id'], comprobante['observacion'], estado_acepta = 'PENDIENTE')
                    else:
                            servicePDV.save_observacion(comprobante)
                    continue

                if not estado_comprobante == 'ACEPTADO':
                    comprobante["observacion"] = f'{tipo} no se encuentra ACEPTADO en el PORTAL ACEPTA. Estado: {estado_comprobante}'
                    if tipo == 'NOTAS':
                        servicePDV.save_observacion_nota(comprobante['id'], comprobante['observacion'], estado_comprobante)
                    else:
                        servicePDV.save_observacion(comprobante)
                logger.warning(f'Estado Portal Acepta: {estado_acepta}')
                comprobante["estado"] = estado_comprobante
            # logger.info(f'Estado Dynamics 365: {estado_acepta}')
            return _comprobantes