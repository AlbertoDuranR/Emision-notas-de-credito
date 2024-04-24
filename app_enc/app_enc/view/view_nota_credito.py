import json
from django.http import JsonResponse
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
            sol_ids = []
            solicitudes = ViewSolicitudNotaDeCredito.objects.filter(sol_estado='VALIDADO', sol_tipo_nc='PDV') # Buscar todas las solicitudes con estado VALIDADO
            if not solicitudes:
                return JsonResponse({'message': 'Sin Solicitudes VALIDADAS'}, status=404)

            solicitudes_ordenadas = solicitudes.order_by('sol_id')
            for solicitud in solicitudes_ordenadas:
                sol_ids.append(solicitud.sol_id)

            try:
                print('create_all_notas_credito')
                ServiceNotaCredito.crear_masivo_notas_de_credito(sol_ids=sol_ids)
                nro_notas_credito = []
                for sol_id in sol_ids:
                    try:
                        solicitud = ViewSolicitudNotaDeCredito.objects.get(sol_id=sol_id, sol_estado='CREADO')
                    except ViewSolicitudNotaDeCredito.DoesNotExist:
                        continue
                    else:
                        if not solicitud and not solicitud.det_nro_nota_credito:
                            continue
                        nro_notas_credito.append(solicitud.det_nro_nota_credito)
                return JsonResponse({'message': f'Se crearon {len(nro_notas_credito)} / {len(sol_ids)}', 'notas_creadas' : nro_notas_credito}, status=200)
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