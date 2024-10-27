#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_board_admin.py
#  Last Modified: 2024-10-26 21:56:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:56:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.metakanban.models.meta_kanban_board_models import MetaKanbanBoard
from apps.metakanban.utils import META_KANBAN_BOARD_ADMIN_LIST, META_KANBAN_BOARD_ADMIN_FILTER, \
    META_KANBAN_BOARD_ADMIN_SEARCH


@admin.register(MetaKanbanBoard)
class MetaKanbanBoardAdmin(admin.ModelAdmin):
    list_display = META_KANBAN_BOARD_ADMIN_LIST
    search_fields = META_KANBAN_BOARD_ADMIN_SEARCH
    list_filter = META_KANBAN_BOARD_ADMIN_FILTER
    ordering = ['id', 'project', 'llm_model', 'title', 'description', 'created_by_user', 'created_at', 'updated_at']
