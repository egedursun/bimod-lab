#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_meeting_transcription_admin.py
#  Last Modified: 2024-10-28 03:43:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 03:43:07
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

from apps.metakanban.models import (
    MetaKanbanMeetingTranscription
)

from apps.metakanban.utils import (
    META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_LIST,
    META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_FILTER,
    META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_SEARCH
)


@admin.register(MetaKanbanMeetingTranscription)
class MetaKanbanMeetingTranscriptionAdmin(admin.ModelAdmin):
    list_display = META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_LIST
    list_filter = META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_FILTER
    search_fields = META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_SEARCH

    ordering = ('-created_at',)
