#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: support_ticket_response_admin.py
#  Last Modified: 2024-09-27 16:47:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:08:58
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.support_system.models import SupportTicketResponse


@admin.register(SupportTicketResponse)
class SupportTicketResponseAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at']
    search_fields = ['ticket__title', 'response']
    date_hierarchy = 'created_at'
