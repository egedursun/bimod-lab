#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: project_admin.py
#  Last Modified: 2024-10-24 22:00:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:00:22
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

from apps.projects.models import ProjectItem

from apps.projects.utils import (
    PROJECT_ITEM_ADMIN_LIST,
    PROJECT_ITEM_ADMIN_FILTER,
    PROJECT_ITEM_ADMIN_SEARCH
)


@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = PROJECT_ITEM_ADMIN_LIST
    list_filter = PROJECT_ITEM_ADMIN_FILTER
    search_fields = PROJECT_ITEM_ADMIN_SEARCH

    ordering = (
        'organization',
        'project_name',
        'project_department',
        'created_at'
    )

