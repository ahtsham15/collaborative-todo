
# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from tasks.consumers import TestConsumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collaborative_todo.settings')

# django_asgi_app = get_asgi_application()

# ws_patterns = [
#     path("ws/test/", TestConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(  # Wrap WebSocket connections with authentication
#         URLRouter(ws_patterns)
#     ),
# })


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from tasks.consumers import TestConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collaborative_todo.settings')

django_asgi_app = get_asgi_application()

# Define your WebSocket routing with dynamic room_name
ws_patterns = [
    # Here <str:room_name> captures dynamic room name (e.g., task list ID)
    path("ws/test/<str:room_name>/", TestConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(ws_patterns)
    ),
})

