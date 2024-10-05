#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: organization_admin.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: organization_admin.py
#  Last Modified: 2024-09-27 17:03:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:07:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.organization.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "address", "industry", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "industry", "created_at", "updated_at")
    search_fields = ("name", "email", "phone", "address", "industry")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ["is_active"]
    list_display_links = ["name"]
    list_select_related = False
    list_display_links_details = False
