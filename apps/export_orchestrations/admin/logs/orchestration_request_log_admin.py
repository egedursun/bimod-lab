#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: orchestration_request_log_admin.py
#  Last Modified: 2024-09-28 15:08:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:52:12
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.export_orchestrations.models import OrchestratorRequestLog


@admin.register(OrchestratorRequestLog)
class OrchestratorRequestLogAdmin(admin.ModelAdmin):
    list_display = ("export_orchestration", "timestamp")
    list_filter = ("export_orchestration", "timestamp")
    search_fields = ("export_orchestration", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
