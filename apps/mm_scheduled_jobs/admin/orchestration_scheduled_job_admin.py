#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_scheduled_job_admin.py
#  Last Modified: 2024-11-14 06:07:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 06:07:06
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

from apps.mm_scheduled_jobs.models import (
    OrchestrationScheduledJob
)

from apps.mm_scheduled_jobs.utils import (
    ORCHESTRATION_SCHEDULED_JOB_ADMIN_LIST,
    ORCHESTRATION_SCHEDULED_JOB_ADMIN_SEARCH,
    ORCHESTRATION_SCHEDULED_JOB_ADMIN_FILTER
)


@admin.register(OrchestrationScheduledJob)
class OrchestrationScheduledJobAdmin(admin.ModelAdmin):
    list_display = ORCHESTRATION_SCHEDULED_JOB_ADMIN_LIST
    search_fields = ORCHESTRATION_SCHEDULED_JOB_ADMIN_SEARCH
    list_filter = ORCHESTRATION_SCHEDULED_JOB_ADMIN_FILTER
