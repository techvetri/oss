from django.urls import re_path
from . import consumers, weblogin

websocket_urlpatterns = [
    re_path(r'ws/admin/', consumers.Consumer.as_asgi(), name="test"),
    re_path(r'ws/login/', weblogin.WebLogin.as_asgi(), name="web-login")
]
