
from django.urls import re_path, path
from config.consumers import LogConsumer, OrchestrationLogConsumer, OrchestrationGenericLogConsumer, \
    VoidForgeOperationLogsConsumer, LeanModLogConsumer

websocket_urlpatterns = [
    re_path(r'ws/logs/(?P<chat_id>\w+)/$', LogConsumer.as_asgi()),
    re_path(r'ws/lean_logs/(?P<lean_chat_id>\w+)/$', LeanModLogConsumer.as_asgi()),

    re_path(r'ws/orchestration_logs/(?P<query_id>\w+)/$', OrchestrationLogConsumer.as_asgi()),
    re_path(r'ws/orchestration_generic_logs/(?P<maestro_id>\w+)/$', OrchestrationGenericLogConsumer.as_asgi()),
    ########
    path('ws/voidforge_operation_logs/', VoidForgeOperationLogsConsumer.as_asgi()),
]
