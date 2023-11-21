from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from core.erp.models import DetTrasladoProd, TrasladoProduc
from core.reportes.forms import ReportForm
#ESTA LIBRERIA PERMITE CONDICIONAR LOS FILTROS CUANDO UNA CONSULTA DA NULOS
from django.db.models.functions import Coalesce

from django.db.models import Sum

class ReportTrasladoView(TemplateView):
    template_name= 'traslados/report_tras.html'

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
                search =  DetTrasladoProd.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(trasproduc__fecha_traslado__range=[start_date, end_date])
                    for t in search:
                        item = {}                  
                        item['prod'] = t.prod.nombre,                 
                        item['proddesc'] = t.prod.descripcion,
                        item['tipo_tras'] = t.trasproduc.tipo_traslado.denominacion,
                        item['codbien'] = t.codbien.codbien,
                        item['fecha'] = t.trasproduc.fecha_traslado.strftime('%Y-%m-%d'),
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
        context['title'] = 'Reporte de Traslados de Productos'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report:traslado_report')
        context['form'] = ReportForm()
        return context