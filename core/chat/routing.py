from django.urls import path
from core.chat.consumers import PrivateChatConsumer

websocket_urlpatterns = [
    path('ws/<int:id>/', PrivateChatConsumer.as_asgi()),
]