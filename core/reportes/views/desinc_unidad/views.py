from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from core.erp.models import DetDesincProd, DesincProduc
from core.reportes.forms import ReportForm
#ESTA LIBRERIA PERMITE CONDICIONAR LOS FILTROS CUANDO UNA CONSULTA DA NULOS
from django.db.models.functions import Coalesce

from django.db.models import Sum

class ReportDesincUnidadView(TemplateView):
    template_name= 'desinc_unidad/report_desinc_unidad.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                position = 1
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search =  DetDesincProd.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(desinc__fecha_desinc__range=[start_date, end_date])
                    for d in search:
                        item = {}                  
                        item['prod'] = d.prod.nombre,
                        item['proddesc'] = d.prod.descripcion,
                        item['tipo_desinc'] = d.desinc.tipo_desinc.denominacion,
                        item['codbien'] = d.codbien.codbien,
                        item['fecha'] = d.desinc.fecha_desinc.strftime('%Y-%m-%d'), 
                        item['position'] = position
                        data.append(item)
                        position += 1                   
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Desincorporación en Unidad'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report:desinc_unidad_report')
        context['form'] = ReportForm()
        return context