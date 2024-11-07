#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_integration_team_admin.py
#  Last Modified: 2024-11-06 17:49:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 17:49:51
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

from apps.meta_integrations.models import MetaIntegrationTeam
from apps.meta_integrations.utils import META_INTEGRATION_TEAM_ADMIN_LIST, META_INTEGRATION_TEAM_ADMIN_FILTER, \
    META_INTEGRATION_TEAM_ADMIN_SEARCH


@admin.register(MetaIntegrationTeam)
class MetaIntegrationTeamAdmin(admin.ModelAdmin):
    list_display = META_INTEGRATION_TEAM_ADMIN_LIST
    list_filter = META_INTEGRATION_TEAM_ADMIN_FILTER
    search_fields = META_INTEGRATION_TEAM_ADMIN_SEARCH
    ordering = ['created_at']
