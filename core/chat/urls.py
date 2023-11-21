from django.urls import path
from core.chat.views import *

app_name = 'chat'

urlpatterns = [
    path('chat/sala/', SalaListView.as_view(), name='sala'),
    path('chat/user/', ChatUserListView.as_view(), name='user'),
]