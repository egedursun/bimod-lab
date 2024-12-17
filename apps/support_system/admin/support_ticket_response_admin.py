#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: support_ticket_response_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.support_system.models import (
    SupportTicketResponse
)

from apps.support_system.utils import (
    SUPPORT_TICKET_RESPONSE_ADMIN_LIST,
    SUPPORT_TICKET_RESPONSE_ADMIN_SEARCH
)


@admin.register(SupportTicketResponse)
class SupportTicketResponseAdmin(admin.ModelAdmin):
    list_display = SUPPORT_TICKET_RESPONSE_ADMIN_LIST
    search_fields = SUPPORT_TICKET_RESPONSE_ADMIN_SEARCH

    date_hierarchy = 'created_at'
