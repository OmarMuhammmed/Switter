import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),

        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(
                websocket_urlpatterns
                ))
        ),
    }
)