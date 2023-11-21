import json
from core.erp.forms import FormCategoria
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.forms import FormCategoria
from core.reportes.forms import FormAction
from core.erp.models import Categoria
from core.audit_log.mixins import AuditMixin

class CategoryListView(LoginRequiredMixin, Perms_Check, FormView):   
    form_class = FormAction
    template_name = 'category/list.html'
    permission_required = 'erp.view_categoria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_categoria',)
                if request.user.has_perms(perms):
                    category = Categoria()                    
                    category.nombre = request.POST.get('nombre')
                    category.save()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción' 

            elif action == 'edit':
                perms = ('erp.change_categoria',)
                if request.user.has_perms(perms):
                    category = Categoria.objects.get(pk=request.POST['id'])
                    category.nombre = request.POST.get('nombre')
                    category.save()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'fields_save':
                changes = json.loads(request.POST['changes'])
                print('SE EJECUTO')
                AuditMixin.fields_save(changes)

            elif action == 'delete':
                perms = ('erp.delete_categoria',)
                if request.user.has_perms(perms):
                    category = Categoria.objects.get(pk=request.POST['id'])
                    category.delete()                   
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'    

            elif action == 'delete_multiple':
                with transaction.atomic():
                    perms = ('erp.delete_categoria',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        category = Categoria.objects.filter(id__in=ids)
                        category.delete()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorías'
        context['entity'] = 'Categorias'
        context['btn_name'] = 'Nueva Categoria'
        context['frmCateg'] = FormCategoria()
        return context