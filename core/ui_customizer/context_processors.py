from crum import get_current_request
from .models import Customizer

def global_data(request):
    user = request.user
    data = {}
    
    if user.is_authenticated:
        settings = Customizer.objects.prefetch_related('user').filter(user_id=user.id)
        if settings:
            for i in settings:
                data['nav_link_theme'] = i.nav_link
                data['brand_logo_theme'] = i.brand_logo_theme
                data['navbar_theme'] = i.navbar_theme
                data['main_theme'] = i.main_theme
                data['sidebar_theme'] = i.sidebar_theme
                data['sidebar_collapse'] = i.sidebar_collapse
                data['sidebar_fixed'] = i.sidebar_fixed
                data['sidebar_nav'] = f'{i.sidebar_flat} {i.sidebar_legacy}'
                data['sidebar_orientation'] = f'{i.sidebar_orientation}/body.html'
        else:
            data['nav_link_theme'] = 'theme_blue'
            data['brand_logo_theme'] = 'theme_dark'
            data['navbar_theme'] = 'theme_blue'
            data['main_theme'] = 'theme_blue'
            data['sidebar_theme'] = 'sidebar-dark-primary'
            data['sidebar_collapse'] = ''
            data['sidebar_fixed'] = 'layout-fixed'
            data['sidebar_nav'] = ''
            data['sidebar_orientation'] = 'vtc/body.html'    
    return {'customize': data}
