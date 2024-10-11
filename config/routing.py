#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: routing.py
#  Last Modified: 2024-10-05 15:31:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:30:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.urls import re_path, path
from config.consumers import LogConsumer, OrchestrationLogConsumer, OrchestrationGenericLogConsumer, \
    VoidForgeOperationLogsConsumer, LeanModLogConsumer

websocket_urlpatterns = [
    re_path(r'ws/logs/(?P<chat_id>\w+)/$', LogConsumer.as_asgi()),
    re_path(r'ws/lean_logs/(?P<lean_chat_id>\w+)/$', LeanModLogConsumer.as_asgi()),
    re_path(r'ws/orchestration_logs/(?P<query_id>\w+)/$', OrchestrationLogConsumer.as_asgi()),
    re_path(r'ws/orchestration_generic_logs/(?P<maestro_id>\w+)/$', OrchestrationGenericLogConsumer.as_asgi()),
    path('ws/voidforge_operation_logs/', VoidForgeOperationLogsConsumer.as_asgi()),
]
