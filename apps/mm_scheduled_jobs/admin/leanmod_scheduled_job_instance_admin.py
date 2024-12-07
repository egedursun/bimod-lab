#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_scheduled_job_instance_admin.py
#  Last Modified: 2024-12-07 14:03:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 14:03:09
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

from apps.mm_scheduled_jobs.models import LeanModScheduledJobInstance

from apps.mm_scheduled_jobs.utils import (
    LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_LIST,
    LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_SEARCH,
    LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_FILTER
)


@admin.register(LeanModScheduledJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_LIST
    search_fields = LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_SEARCH
    list_filter = LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_FILTER
