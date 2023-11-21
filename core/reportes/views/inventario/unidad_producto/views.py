from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from core.erp.models import InventarioBienes, SalidaProduc
from core.reportes.forms import ReporUnidadForm, ReportForm
#ESTA LIBRERIA PERMITE CONDICIONAR LOS FILTROS CUANDO UNA CONSULTA DA NULOS
from django.db.models.functions import Coalesce

from django.db.models import Sum

class ReportUnidadProdView(TemplateView):
    template_name= 'inventario/unidad_prod/reportuni_prod.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                # unidad=request.POST['unidad']
                search =  InventarioBienes.objects.all()
                if len(start_date) and len(end_date):                    
                    search = search.exclude(ult_proc='DESINC').filter(date_joined__range=[start_date, end_date]).order_by('unidad')
                    for i in search:
                        item = {}                  
                        item['unidad'] = i.unidad.nombre                  
                        item['ubica_fisica'] = i.ubica_fisica.nombre
                        item['prod'] = i.prod.nombre +' / '+ i.prod.descripcion
                        item['codbien'] = i.codbien.codbien
                        item['ult_proc'] = i.ult_proc
                        item['tipo_proc'] = i.tipo_proc.denominacion
                        item['date_joined'] = i.date_joined.strftime('%Y-%m-%d')                        
                        # print(item)
                        data.append(item)
                        # else:
                        #     search = search.exclude(ult_proc='DESINC')
                        #     for i in search:
                        #         item = {}
                        #         item['id'] = i.id
                        #         item['unidad'] = i.unidad.nombre                   
                        #         item['ubica_fisica'] = i.ubica_fisica.nombre
                        #         item['prod'] = i.prod.nombre +'/'+ i.prod.descripcion
                        #         item['codbien'] = i.codbien.codbien
                        #         item['ult_proc'] = i.ult_proc
                        #         item['tipo_proc'] = i.tipo_proc.denominacion
                        #         print(item)
                        #         data.append(item)
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario de Unidades'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report:unidad_report')
        context['form'] = ReportForm()
        return context