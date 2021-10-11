from django.urls import re_path

from . import consumer
import codenames.consumer as codenames

websocket_urlpatterns = [
    re_path("ws/chat/(?P<room_id>\w+)/$", consumer.ChatConsumer.as_asgi()),
    re_path("ws/codenames/(?P<room_id>\w+)/$", codenames.CodenamesConsumer.as_asgi()),
]