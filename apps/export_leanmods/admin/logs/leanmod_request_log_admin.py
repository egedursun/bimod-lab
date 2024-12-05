#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_request_log_admin.py
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

from apps.export_leanmods.models import LeanmodRequestLog

from apps.export_leanmods.utils import (
    EXPORT_LEANMOD_REQUEST_LOG_ADMIN_LIST,
    EXPORT_LEANMOD_REQUEST_LOG_ADMIN_FILTER,
    EXPORT_LEANMOD_REQUEST_LOG_ADMIN_SEARCH
)


@admin.register(LeanmodRequestLog)
class LeanmodRequestLogAdmin(admin.ModelAdmin):
    list_display = EXPORT_LEANMOD_REQUEST_LOG_ADMIN_LIST
    list_filter = EXPORT_LEANMOD_REQUEST_LOG_ADMIN_FILTER
    search_fields = EXPORT_LEANMOD_REQUEST_LOG_ADMIN_SEARCH
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]
