from django import template
from crum import get_current_request

register = template.Library()

@register.filter()
def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms


@register.filter(name='has_perms') 
def has_perms(self, request, group, perms ):
    request = get_current_request()
    if 'group' in request.session:
            group = request.session['group']
            perms = self.get_perms()
    return group.permissions.filter(codename=perms).exists()

