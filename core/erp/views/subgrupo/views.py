from core.erp.forms import FormSubGrupo
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import ValidatePermissionRequiredMixin, Perms_Check
from core.erp.models import SubGrupoCtaBienes


class SubGrupoListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = SubGrupoCtaBienes
    template_name = 'subgrupo/list.html'
    permission_required = 'erp.view_subgrupoctabienes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                
                data = []
                for i in SubGrupoCtaBienes.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':

                perms = ('erp.add_subgrupoctabienes',)
                if request.user.has_perms(perms): 
                    subgrupo = SubGrupoCtaBienes.objects.create(
                        denominacion=request.POST['denominacion'],
                        subgrupo=request.POST['subgrupo'],
                        seccion=request.POST['seccion'],
                        cod_grusubgrusec=request.POST['cod_grusubgrusec'],
                        grupo_id=request.POST['grupo']
                    )
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'edit':

                perms = ('erp.change_subgrupoctabienes',)
                if request.user.has_perms(perms): 
                    subgrupo = SubGrupoCtaBienes.objects.get(id=request.POST['id'])
                    subgrupo.denominacion = request.POST['denominacion']
                    subgrupo.subgrupo = request.POST['subgrupo']
                    subgrupo.seccion = request.POST['seccion']
                    subgrupo.cod_grusubgrusec = request.POST['cod_grusubgrusec']
                    subgrupo.grupo_id = request.POST['grupo']
                    subgrupo.save()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'delete':

                perms = ('erp.delete_subgrupoctabienes',)
                if request.user.has_perms(perms): 
                    subgrupo = SubGrupoCtaBienes.objects.select_related('grupo').get(id=request.POST['id'])
                    subgrupo.delete()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de SubGrupos'
        context['entity'] = 'Listado'
        context['btn_name'] = 'Nuevo SubGrupo'
        context['frmSubGrupo'] = FormSubGrupo()
        return context
