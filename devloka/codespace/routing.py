from codespace import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(
        r"ws/codespace/(?P<codespace_id>\w+)/$", consumers.CodeSpaceConsumer.as_asgi()
    ),
]
