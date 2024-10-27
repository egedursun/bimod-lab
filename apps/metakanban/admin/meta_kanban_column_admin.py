#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_column_models.py
#  Last Modified: 2024-10-26 21:57:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:57:03
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

from apps.metakanban.models.meta_kanban_column_models import MetaKanbanStatusColumn
from apps.metakanban.utils import META_KANBAN_STATUS_COLUMN_LIST, META_KANBAN_STATUS_COLUMN_FILTER, \
    META_KANBAN_STATUS_COLUMN_SEARCH


@admin.register(MetaKanbanStatusColumn)
class MetaKanbanStatusColumnAdmin(admin.ModelAdmin):
    list_display = META_KANBAN_STATUS_COLUMN_LIST
    list_filter = META_KANBAN_STATUS_COLUMN_FILTER
    search_fields = META_KANBAN_STATUS_COLUMN_SEARCH
    ordering = ('position_id', 'created_at')
