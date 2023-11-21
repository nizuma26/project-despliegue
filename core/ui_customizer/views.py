import json
from django.db import transaction
from django.utils.timesince import timesince
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .models import *

class CustomizeBasicInterface(View):   
    model = Customizer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add_settings':
                customizer = json.loads(request.POST['settings'])
                settings = Customizer.objects.prefetch_related('user').filter(user_id=self.request.user.id)
                my_id = request.POST['my_id']
                if settings:
                    print('EXISTE LA CONFIGURACIÓN')
                    settings.update(
                        nav_link=customizer['dataOne']['nav_link'], 
                        brand_logo_theme=customizer['dataOne']['brand_logo_theme'], 
                        navbar_theme=customizer['dataOne']['navbar_theme'], 
                        main_theme=customizer['dataOne']['main_color'],
                        sidebar_theme=customizer['dataOne']['sidebar_theme'], 
                        navbar_fixed=customizer['dataOne']['navbar_fixed'], 
                        sidebar_collapse=customizer['dataTwo']['sidebar_options']['collapse'], 
                        sidebar_fixed=customizer['dataTwo']['sidebar_options']['fixed'], 
                        sidebar_flat=customizer['dataTwo']['sidebar_options']['flat'], 
                        sidebar_orientation=customizer['dataTwo']['sidebar_options']['orientation'], 
                        sidebar_legacy=customizer['dataTwo']['sidebar_options']['legacy'], 
                        sidebar_disable_hover=customizer['dataTwo']['sidebar_options']['disable_hover'], 
                        small_body=customizer['dataTwo']['small_text']['body'],
                        small_navbar=customizer['dataTwo']['small_text']['navbar'], 
                        small_brand=customizer['dataTwo']['small_text']['brand'], 
                        small_sidebar_nav=customizer['dataTwo']['small_text']['sidebar_nav'], 
                        small_footer=customizer['dataTwo']['small_text']['footer']
                    )                    
                else:
                    print('NO EXISTE LA CONFIGURACIÓN')
                    custom = Customizer.objects.create(
                        nav_link=customizer['dataOne']['nav_link'],
                        brand_logo_theme=customizer['dataOne']['brand_logo_theme'],
                        navbar_theme=customizer['dataOne']['navbar_theme'],
                        navbar_fixed=customizer['dataOne']['navbar_fixed'],
                        main_theme=customizer['dataOne']['main_color'],
                        sidebar_theme=customizer['dataOne']['sidebar_theme'],
                        sidebar_collapse=customizer['dataTwo']['sidebar_options']['collapse'],
                        sidebar_fixed = customizer['dataTwo']['sidebar_options']['fixed'],
                        sidebar_flat = customizer['dataTwo']['sidebar_options']['flat'],
                        sidebar_orientation=customizer['dataTwo']['sidebar_options']['orientation'],
                        sidebar_legacy = customizer['dataTwo']['sidebar_options']['legacy'],
                        sidebar_disable_hover = customizer['dataTwo']['sidebar_options']['disable_hover'],
                        small_body = customizer['dataTwo']['small_text']['body'],
                        small_navbar = customizer['dataTwo']['small_text']['navbar'],
                        small_brand =customizer['dataTwo']['small_text']['brand'],
                        small_sidebar_nav = customizer['dataTwo']['small_text']['sidebar_nav'],
                        small_footer = customizer['dataTwo']['small_text']['footer'],
                        user_id = self.request.user.id,
                    )

            elif action == 'get_settings':
                # data = {}
                my_id = request.POST['my_id']
                settings = Customizer.objects.prefetch_related('user').filter(user_id=int(my_id))
                if settings:
                    for i in settings:
                        data['value'] = True
                        data['nav_link_theme'] = i.nav_link
                        data['brand_logo_theme'] = i.brand_logo_theme
                        data['navbar_theme'] = i.navbar_theme
                        data['main_color'] = i.main_theme
                        data['sidebar_theme'] = i.sidebar_theme
                        data['navbar_fixed'] = i.navbar_fixed
                        data['sidebar_collapse'] = i.sidebar_collapse
                        data['sidebar_fixed'] = i.sidebar_fixed
                        data['sidebar_flat'] = i.sidebar_flat
                        data['sidebar_orientation'] = i.sidebar_orientation
                        data['sidebar_legacy'] = i.sidebar_legacy
                        data['sidebar_disable_hover'] = i.sidebar_disable_hover
                        data['small_body'] = i.small_body
                        data['small_navbar'] = i.small_navbar
                        data['small_sidebar_nav'] = i.small_sidebar_nav
                        data['small_brand'] = i.small_brand
                        data['small_footer'] = i.small_footer
                else:
                    data['value'] = False
            else:                
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

