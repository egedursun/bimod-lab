#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_change_log_admin.py
#  Last Modified: 2024-10-26 21:56:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:56:55
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

from apps.metakanban.models.meta_kanban_change_log_models import (
    MetaKanbanChangeLog
)

from apps.metakanban.utils import (
    META_KANBAN_CHANGE_LOG_ADMIN_LIST,
    META_KANBAN_CHANGE_LOG_ADMIN_FILTER,
    META_KANBAN_CHANGE_LOG_ADMIN_SEARCH
)


@admin.register(MetaKanbanChangeLog)
class MetaKanbanChangeLogAdmin(admin.ModelAdmin):
    list_display = META_KANBAN_CHANGE_LOG_ADMIN_LIST
    list_filter = META_KANBAN_CHANGE_LOG_ADMIN_FILTER
    search_fields = META_KANBAN_CHANGE_LOG_ADMIN_SEARCH

    ordering = ['-timestamp']
