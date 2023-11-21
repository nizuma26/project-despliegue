import json
from django.conf import settings
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, response
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView
#from django.views.generic import TemplateView

from core.erp.forms import FormControlStock
from core.erp.models import Producto, Almacen, ControlStock
from django.template.loader import get_template
from core.erp.mixins import ValidatePermissionRequiredMixin, Perms_Check
from decimal import Decimal
from django.template import Context


class StockListView(LoginRequiredMixin, Perms_Check, FormView):
    model = ControlStock
    form_class = FormControlStock
    template_name = 'control_stock/list.html'
    permission_required = 'erp.view_controlstock'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']           
            if action == 'searchdata':
                data = []
                queryset = ControlStock.objects.all().prefetch_related('productos')               
                queryset = queryset.filter(almacenes_id__in=request.POST['almacen'])
                for i in queryset:
                    item = {}
                    item['id'] = i.id
                    item['id_prod'] = i.productos.id
                    item['prod'] = i.productos.nombre + ' / ' + i.productos.descripcion
                    item['categorias'] = i.productos.categorias.nombre
                    item['precio'] = i.precio
                    item['stock'] = i.stock_actual
                    item['stock_min'] = i.stock_min
                    item['stock_max'] = i.stock_max
                    data.append(item)
            
            elif action == 'edit':                
                values = json.loads(request.POST['value'])
                prod = list(filter(None, values['values']))
                for i in prod:
                    queryset = ControlStock.objects.filter(id=int(i['id'])).prefetch_related('productos')
                    queryset.update(stock_min=int(i['stockMin']), stock_max=int(i['stockMax']))
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['list_url'] = reverse_lazy('erp:stock_list')
        context['entity'] = 'Productos'
        return context
