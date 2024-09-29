#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: triggered_job_instance_admin.py
#  Last Modified: 2024-09-28 19:54:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:03:55
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
from django.contrib import admin

from apps.mm_triggered_jobs.models import TriggeredJobInstance


@admin.register(TriggeredJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = ['triggered_job', 'status', 'started_at', 'ended_at']
    search_fields = ['triggered_job', 'status', 'started_at', 'ended_at']
    list_filter = ['triggered_job', 'status', 'started_at', 'ended_at']
