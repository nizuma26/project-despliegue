from django.urls import path
from core.group.views import *

app_name = 'group'


urlpatterns = [
    # groups
    path('list/', GroupsListView.as_view(), name='group_list'),
    path('add/', GroupsCreateView.as_view(), name='group_create'),
    path('update/<int:pk>/', GroupsUpdateView.as_view(), name='group_update'),
    path('delete/<int:pk>/', GroupsDeleteView.as_view(), name='group_delete'),
    #path('group_permissions/<int:group_id>/', group_permissions, name='group_permissions'),
    #path('permisos_grupo/<int:pk>/', permisos_grupo, name='permisos_grupo'),

]


