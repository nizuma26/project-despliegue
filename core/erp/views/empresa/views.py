from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.erp.forms import EmpresaForm
from core.erp.mixins import ValidatePermissionRequiredMixin, Perms_Check
from core.erp.models import Empresa

class EmpresaListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = Empresa
    template_name = 'empresa/list.html'
    permission_required = 'erp.view_empresa'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Empresa.objects.all():
                    item = {}
                    item['id'] = i.id
                    item['nombre'] = i.nombre
                    item['documento'] = i.documento
                    item['representante'] = i.representante
                    item['email'] = i.email
                    item['tlflocal'] = i.tlflocal
                    item['logo'] = i.get_logo()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Información de la Institución'
        context['create_url'] = reverse_lazy('erp:empresa_update')
        context['list_url'] = reverse_lazy('erp:empresa_list')
        context['entity'] = 'Empresa'
        context['btn_name'] = 'Adjuntar Información'
        return context

class EmpresaUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/create.html'
    permission_required = 'erp.change_empresa'
    success_url = reverse_lazy('erp:empresa_list')


    def get_object(self, queryset=None):
        empresa = Empresa.objects.all()
        if empresa.exists():
            return empresa[0]
        return Empresa()


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                if instance.pk is not None:
                    form = EmpresaForm(request.POST, request.FILES, instance=instance)
                    data = form.save()
                else:
                    form = EmpresaForm(request.POST, request.FILES)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Institución'
        context['title'] = 'Registro de datos de la institución'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context