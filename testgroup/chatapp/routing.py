from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/chatapp/(?P<room_name>\w+)', consumer.ChatRoomConsumer.as_asgi()),
]