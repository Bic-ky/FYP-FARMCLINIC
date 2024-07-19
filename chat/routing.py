from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chat/', consumers.ChatConsumer.as_asgi()),
]

# chat/routing.py
# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]