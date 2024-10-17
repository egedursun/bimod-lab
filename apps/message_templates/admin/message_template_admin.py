#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: message_template_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.contrib import admin

from apps.message_templates.models import MessageTemplate
from apps.message_templates.utils import MESSAGE_TEMPLATE_ADMIN_LIST, MESSAGE_TEMPLATE_ADMIN_FILTER, \
    MESSAGE_TEMPLATE_ADMIN_SEARCH


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = MESSAGE_TEMPLATE_ADMIN_LIST
    search_fields = MESSAGE_TEMPLATE_ADMIN_SEARCH
    list_filter = MESSAGE_TEMPLATE_ADMIN_FILTER
    ordering = ["-created_at"]
