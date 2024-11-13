#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-23 17:33:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 17:33:48
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

from apps.metakanban.views import (MetaKanbanView_TaskCreate, MetaKanbanView_TaskDelete,
                                   MetaKanbanView_TaskDetailAndUpdate, MetaKanbanView_TaskMove,
                                   MetaKanbanView_ColumnConfirmDelete, MetaKanbanView_BoardConfirmDelete,
                                   MetaKanbanView_BoardList, MetaKanbanView_BoardCreate, MetaKanbanView_BoardDetail,
                                   MetaKanbanView_ColumnCreate, MetaKanbanView_ColumnUpdate,
                                   MetaKanbanView_BoardUpdate, MetaKanbanView_TaskAssign, MetaKanbanView_LabelList,
                                   MetaKanbanView_LabelCreate, MetaKanbanView_LabelDelete, MetaKanbanView_LabelUpdate,
                                   MetaKanbanView_ColumnMove, MetaKanbanView_AgentCommunication,
                                   MetaKanbanView_BoardLogList, MetaKanbanView_MeetingRecordingAudioAIDelivery,
                                   MetaKanbanView_MeetingTranscriptionAIImplement,
                                   MetaKanbanView_MeetingTranscriptionList, MetaKanbanView_MeetingTranscriptionDelete,
                                   MetaKanbanView_MeetingRegenerateAPIKey, MetaKanbanView_ConnectAssistantToMetaKanban,
                                   MetaKanbanView_AssistantConnectionDelete)

app_name = 'metakanban'

urlpatterns = [
    # Board: All TemplateView
    path("board/list/", MetaKanbanView_BoardList.as_view(
        template_name="metakanban/board/list_boards.html"), name="board_list"),
    path("board/create/", MetaKanbanView_BoardCreate.as_view(
        template_name="metakanban/board/create_board.html"), name="board_create"),
    path("board/detail/<int:board_id>/", MetaKanbanView_BoardDetail.as_view(
        template_name="metakanban/board/detail_board.html"), name="board_detail"),
    path("board/update/<int:board_id>/", MetaKanbanView_BoardUpdate.as_view(
        template_name="metakanban/board/update_board_info.html"), name="board_update"),
    path("board/delete/<int:board_id>/", MetaKanbanView_BoardConfirmDelete.as_view(
        template_name="metakanban/board/confirm_delete_board.html"), name="board_delete"),

    # Label: Manager Page Template View / Create, Update, Delete HTTP Views
    path("label/list/<int:board_id>/", MetaKanbanView_LabelList.as_view(
        template_name="metakanban/label/add_update_list_delete_labels.html"), name="label_list"),
    path("label/create/<int:board_id>/", MetaKanbanView_LabelCreate.as_view(), name="label_create"),
    path("label/update/<int:board_id>/<int:label_id>/", MetaKanbanView_LabelUpdate.as_view(), name="label_update"),
    path("label/delete/<int:board_id>/<int:label_id>/", MetaKanbanView_LabelDelete.as_view(), name="label_delete"),

    # Column: Create, Update, Delete HTTP Views
    path("column/create/", MetaKanbanView_ColumnCreate.as_view(), name="column_create"),
    path("column/update/", MetaKanbanView_ColumnUpdate.as_view(), name="column_update"),
    path("column/move/", MetaKanbanView_ColumnMove.as_view(), name="column_move"),
    path("column/delete/", MetaKanbanView_ColumnConfirmDelete.as_view(), name="column_delete"),

    # Task: Create, Update, Delete, Move, Assign HTTP Views
    path("task/create/", MetaKanbanView_TaskCreate.as_view(), name="task_create"),
    path("task/move/", MetaKanbanView_TaskMove.as_view(), name="task_move"),
    path("task/assign/", MetaKanbanView_TaskAssign.as_view(), name="task_assign"),
    path("task/delete/", MetaKanbanView_TaskDelete.as_view(), name="task_delete"),
    path("task/detail/", MetaKanbanView_TaskDetailAndUpdate.as_view(), name="task_detail"),

    # Agent Communication: TemplateView
    path("agent/communication/", MetaKanbanView_AgentCommunication.as_view(
        template_name="metakanban/agent/agent_communication.html"), name="agent_communication"),

    # Board Logs: TemplateView
    path("board/logs/<int:board_id>/", MetaKanbanView_BoardLogList.as_view(
        template_name="metakanban/log/metakanban_board_logs.html"), name="board_logs"),

    # Connect Assistant to MetaKanban
    path("connect/assistant/", MetaKanbanView_ConnectAssistantToMetaKanban.as_view(
        template_name="metakanban/connect_assistant/connect_assistant_to_metakanban.html"
    ), name="connect_assistant"),
    path("disconnect/assistant/<int:pk>/", MetaKanbanView_AssistantConnectionDelete.as_view(),
         name="disconnect_assistant"),

    ###############################################################################################################

    # Meeting Recording Audio AI Delivery: HTTP Endpoint Retriever
    path("meeting/recording/delivery/", MetaKanbanView_MeetingRecordingAudioAIDelivery.as_view(),
         name="meeting_recording_delivery"),

    path("meeting/transcription/list/<int:board_id>/", MetaKanbanView_MeetingTranscriptionList.as_view(
        template_name="metakanban/meeting/meeting_transcriptions_list.html"
    ), name="meeting_transcription_list"),

    path("meeting/transcription/implement/<int:transcription_id>/", MetaKanbanView_MeetingTranscriptionAIImplement.as_view(),
            name="meeting_transcription_implement"),
    path("meeting/transcription/delete/<int:transcription_id>/", MetaKanbanView_MeetingTranscriptionDelete.as_view(),
            name="meeting_transcription_delete"),
    path("meeting/regenerate/api_key/", MetaKanbanView_MeetingRegenerateAPIKey.as_view(),
            name="meeting_regenerate_api_key"),

    ###############################################################################################################
]
