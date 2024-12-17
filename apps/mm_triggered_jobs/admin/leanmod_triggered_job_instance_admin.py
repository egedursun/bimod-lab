#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_triggered_job_instance_admin.py
#  Last Modified: 2024-12-07 17:08:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 17:08:28
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

from apps.mm_triggered_jobs.models import (
    LeanModTriggeredJobInstance
)

from apps.mm_triggered_jobs.utils import (
    LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_LIST,
    LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_SEARCH,
    LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_FILTER
)


@admin.register(LeanModTriggeredJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_LIST
    search_fields = LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_SEARCH
    list_filter = LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_FILTER
