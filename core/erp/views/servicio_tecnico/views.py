from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from core.erp.models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView

class SoporteListView(TemplateView):
    template_name = 'servicio_tecnico/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)        


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Recepcion de Soporte'
        context['btn_name'] = 'Nuevo Registro'
        context['create_url'] = reverse_lazy('erp:soporte_create')        
        return context

class SoporteCreateView(TemplateView):
    template_name = 'servicio_tecnico/create.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)        


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Recepcion de Soporte'
        context['list_url'] = reverse_lazy('erp:soporte_list')
        context['entity'] = 'Recepción de Soporte'
        return context

