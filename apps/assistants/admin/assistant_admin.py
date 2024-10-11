#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: assistant_admin.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
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

from apps.assistants.models import Assistant
from apps.assistants.utils import AGENT_ADMIN_DISPLAY_FIELDS, AGENT_ADMIN_FILTER_FIELDS, AGENT_ADMIN_SEARCH_FIELDS


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = AGENT_ADMIN_DISPLAY_FIELDS
    list_filter = AGENT_ADMIN_FILTER_FIELDS
    search_fields = AGENT_ADMIN_SEARCH_FIELDS
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
