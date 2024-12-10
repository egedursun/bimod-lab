#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_elite_agent_admin.py
#  Last Modified: 2024-10-22 18:31:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:31:40
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

from apps.binexus.models import BinexusEliteAgent

from apps.binexus.utils import (
    BINEXUS_ELITE_AGENT_ADMIN_LIST,
    BINEXUS_ELITE_AGENT_ADMIN_FILTER,
    BINEXUS_ELITE_AGENT_ADMIN_SEARCH
)


@admin.register(BinexusEliteAgent)
class BinexusEliteAgentAdmin(admin.ModelAdmin):
    list_display = BINEXUS_ELITE_AGENT_ADMIN_LIST
    list_filter = BINEXUS_ELITE_AGENT_ADMIN_FILTER
    search_fields = BINEXUS_ELITE_AGENT_ADMIN_SEARCH

    ordering = ['-created_at']
