#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: user_permission_admin.py
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


from django.contrib import admin

from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import USER_PERMISSIONS_ADMIN_LIST, USER_PERMISSIONS_ADMIN_FILTER, \
    USER_PERMISSIONS_ADMIN_SEARCH


@admin.register(UserPermission)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = USER_PERMISSIONS_ADMIN_LIST
    list_filter = USER_PERMISSIONS_ADMIN_FILTER
    search_fields = USER_PERMISSIONS_ADMIN_SEARCH
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
