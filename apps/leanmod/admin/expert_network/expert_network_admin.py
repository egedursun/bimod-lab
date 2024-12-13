#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: expert_network_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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

from apps.leanmod.models import (
    ExpertNetwork
)

from apps.leanmod.utils import (
    EXPERT_NETWORK_ADMIN_LIST,
    EXPERT_NETWORK_ADMIN_FILTER,
    EXPERT_NETWORK_ADMIN_SEARCH
)


@admin.register(ExpertNetwork)
class ExpertNetworkAdmin(admin.ModelAdmin):
    list_display = EXPERT_NETWORK_ADMIN_LIST
    list_filter = EXPERT_NETWORK_ADMIN_FILTER
    search_fields = EXPERT_NETWORK_ADMIN_SEARCH

    date_hierarchy = "created_at"
    ordering = ["-created_at"]
