import json
from inertia import render
from django.http import HttpResponse,JsonResponse
from django.middleware.csrf import get_token
from ..models.model_view_solicitudes_nota_de_credito import ViewSolicitudNotaDeCredito
from ..services.service_nota_credito import ServiceNotaCredito
from ..services.service_dynamics import ServiceDynamics

ServiceNotaCredito = ServiceNotaCredito()
serviceDynamics = ServiceDynamics()

class ViewNotaCredito:
    def create_nota_credito(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("", request.body.decode('utf-8'))
            form_request = json.loads(form_request)
            try:
                ServiceNotaCredito.crear_nota_credito(sol_id=form_request['id'])
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print('Expection create_nota_credito:', e)
                return JsonResponse({'message': e.message, 'estado': e.estado, 'step_rpa': e.step}, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)

    def create_all_notas_credito(request):
        if request.method == "POST":
            sol_ids = [] # [{'id': 1, 'nro_comprobante': 'BG02-00052743', 'estado': 'ACEPTADO', 'observacion': ''},]
            solicitudes = ViewSolicitudNotaDeCredito.objects.filter(sol_estado='VALIDADO', sol_tipo_nc='PDV') # Buscar todas las solicitudes con estado VALIDADO
            if not solicitudes:
                return
            for solicitud in solicitudes:
                sol_ids.append(solicitud.sol_id)

            try:
                print('create_all_notas_credito')
                # ServiceNotaCredito.crear_nota_credito(sol_id=form_request['id'])
                ServiceNotaCredito.crear_masivo_notas_de_credito(sol_ids=sol_ids)
                return JsonResponse({'message': 'Datos procesados'}, status=200)
            except Exception as e:
                print('Expection create_nota_credito:', e)
                return JsonResponse({'message': e.message }, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)

    def retry_create_nota_credito(request):
        if request.method == "POST":
            # Transform data
            form_request= str.join("", request.body.decode('utf-8'))
            form_request = json.loads(form_request)
            print(form_request)
            try:
                ServiceNotaCredito.reintentar_crear_nota_credito(sol_id=form_request['id'])
                return JsonResponse({'message': 'Datos procesados correctamente'}, status=200)
            except Exception as e:
                print('Expection retry_create_nota_credito:', e)
                return JsonResponse({'message': e.message, 'estado': e.estado, 'step_rpa': e.step}, status=404)
        else:
            return JsonResponse({'message': 'Error al procesar los datos'}, status=404)