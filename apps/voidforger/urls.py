#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-14 21:28:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 21:28:03
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.urls import path

from apps.voidforger.views import (VoidForgerView_ListVoidForgerAutoExecutionLogs,
                                   VoidForgerView_ManualTriggerVoidForgerRun,
                                   VoidForgerView_RefreshVoidForgerConnections, VoidForgerView_DeleteVoidForgerChat,
                                   VoidForgerView_AutoRunVoidForger, VoidForgerView_PurgeAutoExecutionLogs,
                                   VoidForgerView_PurgeActionMemoryLogs, VoidForgerView_ListActionMemoryLogs,
                                   VoidForgerView_Configuration)

app_name = 'voidforger'

urlpatterns = [
    # Configuration-related
    path("configuration/", VoidForgerView_Configuration.as_view(
        template_name="voidforger/configuration/voidforger_configuration.html"), name="configuration"),
    path("connections/refresh/<int:voidforger_id>/", VoidForgerView_RefreshVoidForgerConnections.as_view(),
         name="refresh_connections"),
    path("auto/run/<int:voidforger_id>/", VoidForgerView_AutoRunVoidForger.as_view(), name="auto_run"),
    path("manual/run/<int:voidforger_id>/", VoidForgerView_ManualTriggerVoidForgerRun.as_view(), name="manual_run"),

    # Logs-related
    path("auto_execution/logs/", VoidForgerView_ListVoidForgerAutoExecutionLogs.as_view(
        template_name="voidforger/logs/list_auto_execution_logs.html"), name="list_auto_execution_logs"),
    path("action_memory/logs/", VoidForgerView_ListActionMemoryLogs.as_view(
        template_name="voidforger/logs/list_action_memory_logs.html"), name="list_action_memory_logs"),
    path("auto_execution/logs/purge/<int:voidforger_id>/", VoidForgerView_PurgeAutoExecutionLogs.as_view(),
         name="purge_auto_execution_logs"),
    path("action_memory/logs/purge/<int:voidforger_id>/", VoidForgerView_PurgeActionMemoryLogs.as_view(),
         name="purge_action_memory_logs"),

    # Chat-related
    path("chat/delete/<int:pk>/", VoidForgerView_DeleteVoidForgerChat.as_view(
        template_name="voidforger/chats/voidforger_confirm_delete_chat.html"
    ), name="delete_chat"),
]
