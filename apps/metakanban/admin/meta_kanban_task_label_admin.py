#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_task_label_admin.py
#  Last Modified: 2024-10-27 00:31:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 00:31:10
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

from apps.metakanban.models import MetaKanbanTaskLabel
from apps.metakanban.utils import META_KANBAN_TASK_LABEL_ADMIN_LIST, META_KANBAN_TASK_LABEL_ADMIN_FILTER, \
    META_KANBAN_TASK_LABEL_ADMIN_SEARCH


@admin.register(MetaKanbanTaskLabel)
class MetaKanbanTaskLabelAdmin(admin.ModelAdmin):
    list_display = META_KANBAN_TASK_LABEL_ADMIN_LIST
    list_filter = META_KANBAN_TASK_LABEL_ADMIN_FILTER
    search_fields = META_KANBAN_TASK_LABEL_ADMIN_SEARCH
    ordering = ('-created_at',)
