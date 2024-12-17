#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: team_admin.py
#  Last Modified: 2024-10-24 22:00:26
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:00:26
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

from apps.projects.models import (
    ProjectTeamItem
)

from apps.projects.utils import (
    PROJECT_TEAM_ITEM_ADMIN_LIST,
    PROJECT_TEAM_ITEM_ADMIN_FILTER,
    PROJECT_TEAM_ITEM_ADMIN_SEARCH
)


@admin.register(ProjectTeamItem)
class ProjectTeamItemAdmin(admin.ModelAdmin):
    list_display = PROJECT_TEAM_ITEM_ADMIN_LIST
    list_filter = PROJECT_TEAM_ITEM_ADMIN_FILTER
    search_fields = PROJECT_TEAM_ITEM_ADMIN_SEARCH

    ordering = (
        'project',
        'team_name',
        'team_lead',
        'created_by_user',
        'created_at'
    )
