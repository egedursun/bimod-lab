#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_triggered_job_admin.py
#  Last Modified: 2024-11-14 07:19:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 07:19:14
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

from apps.mm_triggered_jobs.models import OrchestrationTriggeredJob
from apps.mm_triggered_jobs.utils import ORCHESTRATION_TRIGGERED_JOB_ADMIN_LIST, \
    ORCHESTRATION_TRIGGERED_JOB_ADMIN_SEARCH, ORCHESTRATION_TRIGGERED_JOB_ADMIN_FILTER


@admin.register(OrchestrationTriggeredJob)
class OrchestrationTriggeredJobAdmin(admin.ModelAdmin):
    list_display = ORCHESTRATION_TRIGGERED_JOB_ADMIN_LIST
    search_fields = ORCHESTRATION_TRIGGERED_JOB_ADMIN_SEARCH
    list_filter = ORCHESTRATION_TRIGGERED_JOB_ADMIN_FILTER
