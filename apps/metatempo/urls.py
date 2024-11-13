#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-28 19:35:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:35:45
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

from apps.metatempo.views import (MetaTempoView_ConnectionRegenerateAPIKey, MetaTempoView_TriggerManualAnalysis,
                                  MetaTempoView_ConnectionConfirmDelete, MetaTempoView_ConnectionList,
                                  MetaTempoView_ConnectionCreate, MetaTempoView_ConnectionUpdate,
                                  MetaTempoView_MainBoard, MetaTempoView_PurgeLogs, MetaTempoView_ScreenshotDelivery,
                                  MetaTempoView_AgentCommunication, MetaTempoView_GetConnectionConfig,
                                  MetaTempoView_ConnectAssistantToMetaTempo, MetaTempoView_AssistantConnectionDelete)

app_name = 'metatempo'

urlpatterns = [
    path("connection/create/", MetaTempoView_ConnectionCreate.as_view(
        template_name="metatempo/connection/create_metatempo_connection.html"), name="connection_create"),
    path("connection/list/", MetaTempoView_ConnectionList.as_view(
        template_name="metatempo/connection/list_metatempo_connections.html"), name="connection_list"),
    path("connection/update/<int:connection_id>/", MetaTempoView_ConnectionUpdate.as_view(
        template_name="metatempo/connection/update_metatempo_connection.html"), name="connection_update"),
    path("connection/confirm_delete/<int:connection_id>/", MetaTempoView_ConnectionConfirmDelete.as_view(
        template_name="metatempo/connection/confirm_delete_metatempo_connection.html"),
         name="connection_confirm_delete"),
    path("connection/regenerate_api_key/<int:connection_id>/", MetaTempoView_ConnectionRegenerateAPIKey.as_view(),
         name="connection_regenerate_api_key"),

    # A.K.A Detail Connection Page :-> is accessible from 'connection/list/' page.
    path("board/main/<int:connection_id>/", MetaTempoView_MainBoard.as_view(
        template_name="metatempo/board/metatempo_main_board.html"), name="main_board"),
    path("board/analysis/overall/trigger/<int:connection_id>/", MetaTempoView_TriggerManualAnalysis.as_view(),
         name="trigger_manual_analysis"),
    path("board/logs/purge/<int:connection_id>/", MetaTempoView_PurgeLogs.as_view(), name="purge_logs"),

    # AI Assistant
    path("agent/communication/", MetaTempoView_AgentCommunication.as_view(
        template_name="metatempo/agent/agent_communication.html"), name="agent_communication"),

    # Connect Assistant to MetaTempo
    path("connect/assistant/", MetaTempoView_ConnectAssistantToMetaTempo.as_view(
        template_name="metatempo/connect_assistant/connect_assistant_to_metatempo.html"
    ), name="connect_assistant"),
    path("disconnect/assistant/<int:pk>/", MetaTempoView_AssistantConnectionDelete.as_view(),
         name="disconnect_assistant"),

    ##############################################################################################################

    path("tempo/screenshot/delivery/", MetaTempoView_ScreenshotDelivery.as_view(), name="screenshot_delivery"),
    path("tempo/connection/config/", MetaTempoView_GetConnectionConfig.as_view(), name="get_connection_config"),
]
