#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: scheduled_job_instance_admin.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.mm_scheduled_jobs.models import ScheduledJobInstance


@admin.register(ScheduledJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = ['scheduled_job', 'status', 'started_at', 'ended_at']
    search_fields = ['scheduled_job', 'status', 'started_at', 'ended_at']
    list_filter = ['scheduled_job', 'status', 'started_at', 'ended_at']
