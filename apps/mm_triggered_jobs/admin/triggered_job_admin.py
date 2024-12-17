#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: triggered_job_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.mm_triggered_jobs.utils import (
    TRIGGERED_JOB_ADMIN_LIST,
    TRIGGERED_JOB_ADMIN_SEARCH,
    TRIGGERED_JOB_ADMIN_FILTER
)

from django.contrib import admin

from apps.mm_triggered_jobs.models import (
    TriggeredJob
)


@admin.register(TriggeredJob)
class TriggeredJobAdmin(admin.ModelAdmin):
    list_display = TRIGGERED_JOB_ADMIN_LIST
    search_fields = TRIGGERED_JOB_ADMIN_SEARCH
    list_filter = TRIGGERED_JOB_ADMIN_FILTER
