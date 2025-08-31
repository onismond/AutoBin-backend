from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/bin-updates/$", consumers.BinConsumer.as_asgi()),
]