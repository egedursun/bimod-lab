#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: harmoniq_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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

from apps.harmoniq.models import Harmoniq
from apps.harmoniq.utils import HARMONIQ_AGENT_ADMIN_LIST, HARMONIQ_AGENT_ADMIN_SEARCH, HARMONIQ_AGENT_ADMIN_FILTER


@admin.register(Harmoniq)
class HarmoniqAdmin(admin.ModelAdmin):
    list_display = HARMONIQ_AGENT_ADMIN_LIST
    list_filter = HARMONIQ_AGENT_ADMIN_FILTER
    search_fields = HARMONIQ_AGENT_ADMIN_SEARCH
    ordering = ['-created_at']
