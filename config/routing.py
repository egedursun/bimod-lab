
from django.urls import re_path
from config.consumers import LogConsumer, OrchestrationLogConsumer, OrchestrationGenericLogConsumer

websocket_urlpatterns = [
    re_path(r'ws/logs/(?P<chat_id>\w+)/$', LogConsumer.as_asgi()),
    re_path(r'ws/orchestration_logs/(?P<query_id>\w+)/$', OrchestrationLogConsumer.as_asgi()),
    re_path(r'ws/orchestration_generic_logs/(?P<maestro_id>\w+)/$', OrchestrationGenericLogConsumer.as_asgi()),
]
