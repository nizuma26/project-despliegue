import json
from django.db import transaction
from core.aprobaciones.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from core.erp.mixins import Perms_Check
from core.aprobaciones.forms import ManageRequestForm
from core.solicitudes.models import *

class ManageRequest(Perms_Check, FormView):
    model = Aprobaciones
    permission_required = 'solicitudes.approve_solicitudes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'manage_state':
                print('FUNCIONO')
                
                with transaction.atomic():
                    new_status = request.POST['new_status']
                    motive = request.POST['motive']
                    id = request.POST['id']
                    type = request.POST['type']
                    print('TYPE: ', type)
                    
                    code = Solicitudes.objects.get(id=id)
                    code.estado = new_status
                    code.save()
                    
                    if new_status == 'APROBADO':
                        if type == 'EN_DEPOSITO':
                            cantidad_aprobada = json.loads(request.POST['cantidad_aprobada'])
                            for i in cantidad_aprobada:
                                detail = DetSolicitud.objects.prefetch_related('solicitud','productos','inventario').filter(solicitud_id=code.id, 
                                productos_id=int(i['prod_id']))
                                detail.update(cantidad_aprobada=int(i['cantidad_aprobada']))
                                print('PRODUCTOS', detail)
                                print('APROBADAS', i['cantidad_aprobada'])
                        else:
                            aprobados = json.loads(request.POST['aprobados'])
                            print('APROBADOS: ', aprobados)
                            for c in aprobados:
                                inv = DetSolicitud.objects.prefetch_related('inventario').filter(solicitud_id=code.id, 
                                inventario__codbien_id=c)
                                for i in inv:
                                    inv.update(aprobado=True)
                                    print('INV: ', i.inventario.codbien.codbien)

                    Aprobaciones.objects.create(
                        user_id=self.request.user.id,
                        accion=new_status,
                        motivo=motive,
                        operacion='Solicitud de movimiento',
                        codigo=code.codigo
                    )
                    data = {'type': 'status_request_notification', 
                            'url': f'/solicitudes/solicitud/detail/{id}', 
                            'message': f'Su solicitud ha sido {new_status.lower()}', 
                            'title': f'Solicitud {code.codigo}', 
                            'user_id': code.user.id, 
                            'state': code.estado,
                            }
                           
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    