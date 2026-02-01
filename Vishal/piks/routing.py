from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Room name ke basis par connection handle hoga
    #re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_view()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
