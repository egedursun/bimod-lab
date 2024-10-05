#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: brainstorming_session_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib import admin

from apps.brainstorms.models import BrainstormingSession


@admin.register(BrainstormingSession)
class BrainstormingSessionAdmin(admin.ModelAdmin):
    list_display = ['session_name', 'organization', 'llm_model', 'created_by_user', 'created_at']
    list_filter = ['organization', 'llm_model', 'created_by_user', 'created_at']
    search_fields = ['session_name', 'organization__name', 'llm_model__nickname', 'created_by_user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
