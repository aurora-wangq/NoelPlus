from django.urls import path
from chat import consumers

websocket_urlpatterns = {
    path('', consumers.ChatConsumer.as_asgi()),
}
