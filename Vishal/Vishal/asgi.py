import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import piks.routing 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vishal.settings')

application = ProtocolTypeRouter({
    # Normal HTTP requests ke liye
    "http": get_asgi_application(),
    
    # WebSocket requests ke liye
    "websocket": AuthMiddlewareStack(
        URLRouter(
            piks.routing.websocket_urlpatterns
        )
    ),
})