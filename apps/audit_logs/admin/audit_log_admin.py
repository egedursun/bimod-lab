#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: audit_log_admin.py
#  Last Modified: 2024-10-11 05:23:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-11 05:23:08
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

from apps.audit_logs.models import AuditLog
from apps.audit_logs.utils import AUDIT_LOG_ADMIN_LIST, AUDIT_LOG_ADMIN_SEARCH, AUDIT_LOG_ADMIN_FILTER


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = AUDIT_LOG_ADMIN_LIST
    search_fields = AUDIT_LOG_ADMIN_SEARCH
    list_filter = AUDIT_LOG_ADMIN_FILTER
    ordering = ('-timestamp',)
