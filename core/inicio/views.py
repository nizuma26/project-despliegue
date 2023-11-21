from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.erp.models import *
from core.ui_customizer.models import Customizer
from core.user.models import *
from django.views.generic import TemplateView

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)        

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_incorp_year_month':
                data  = { 
                    'data': {
                    'name': 'Nº de Items Incorporados',
                    'showInLegend': False,
                    'data': self.get_graph_incorp_year_month()
                    },
                }
                #print(self.get_total_incorp_year())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_graph_incorp_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                products = DetIngresoProduc.objects.select_related('ingresoPro').prefetch_related('prod').all()
                incorp = products.filter(ingresoPro__estado="APROBADO", ingresoPro__fecha_ingreso__year=year, ingresoPro__fecha_ingreso__month=m).aggregate(r=Coalesce(Sum('cant'), 0)).get('r')
                data.append(incorp)
        except:
            pass
        return data

    # def get_total_incorp_year(self):
    #     data = []
    #     try:
    #         year = datetime.now().year
    #         for m in range(1, 13):
    #             total = IngresoProduc.objects.filter(fecha_ingreso__year=year, fecha_ingreso__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
    #             data.append(float(total))
    #     except:
    #         pass
    #     return data

    def movements(self):
        data = {
            'incorp': IngresoProduc.objects.filter(estado='POR APROBAR').count(),
            'dist': SalidaProduc.objects.filter(estado='POR APROBAR').count(),
            'tras': TrasladoProduc.objects.filter(estado='POR APROBAR').count(),
            'desinc': DesincProduc.objects.filter(estado='POR APROBAR').count(),
        }
        return data       

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movements'] = self.movements()
        context['users'] = User.objects.filter(is_active=1).count()
        context['products'] = Producto.objects.filter(activo=1)
        context['year'] = datetime.now().year
        context['title'] = 'Dashboard'
        context['entity'] = 'Dashboard'
        return context

class land_page(TemplateView):
    template_name = 'land_page.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)   


def page_not_found404(request, exception):
    return render(request, '404.html')

