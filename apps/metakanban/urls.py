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

from apps.metakanban.views import (MetaKanbanView_TaskCreate, MetaKanbanView_CommentCreate,
                                   MetaKanbanView_CommentDelete, MetaKanbanView_TaskDelete,
                                   MetaKanbanView_TaskDetailAndUpdate, MetaKanbanView_TaskMove,
                                   MetaKanbanView_ColumnConfirmDelete, MetaKanbanView_BoardConfirmDelete,
                                   MetaKanbanView_BoardList, MetaKanbanView_BoardCreate, MetaKanbanView_BoardDetail,
                                   MetaKanbanView_ColumnCreate, MetaKanbanView_ColumnUpdate,
                                   MetaKanbanView_CommentUpdate, MetaKanbanView_BoardUpdate,
                                   MetaKanbanView_ChangeLogList)

app_name = 'metakanban'

urlpatterns = [
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

    path("column/create/<int:board_id>/", MetaKanbanView_ColumnCreate.as_view(
        template_name="metakanban/column/create_board_column.html"), name="column_create"),
    path("column/update/<int:board_id>/<int:column_id>/", MetaKanbanView_ColumnUpdate.as_view(
        template_name="metakanban/column/update_board_column.html"), name="column_update"),
    path("column/delete/<int:board_id>/<int:column_id>/", MetaKanbanView_ColumnConfirmDelete.as_view(
        template_name="metakanban/column/confirm_delete_board_column.html"), name="column_delete"),

    path("task/create/<int:board_id>/", MetaKanbanView_TaskCreate.as_view(), name="task_create"),
    path("task/move/<int:board_id>/<int:task_id>/", MetaKanbanView_TaskMove.as_view(), name="task_move"),
    path("task/delete/<int:board_id>/<int:task_id>/", MetaKanbanView_TaskDelete.as_view(), name="task_delete"),
    path("task/detail/<int:board_id>/<int:task_id>/", MetaKanbanView_TaskDetailAndUpdate.as_view(
        template_name="metakanban/task/detail_and_update_task.html"
    ), name="task_detail"),

    path("comment/create/<int:board_id>/<int:task_id>/", MetaKanbanView_CommentCreate.as_view(),
         name="comment_create"),
    path("comment/update/<int:board_id>/<int:task_id>/<int:comment_id>/", MetaKanbanView_CommentUpdate.as_view(),
         name="comment_update"),
    path("comment/delete/<int:board_id>/<int:task_id>/<int:comment_id>/", MetaKanbanView_CommentDelete.as_view(),
         name="comment_delete"),

    path("changelog/list/<int:board_id>/", MetaKanbanView_ChangeLogList.as_view(
        template_name="metakanban/change_log/list_change_logs.html"
    ), name="changelog_list"),
]
