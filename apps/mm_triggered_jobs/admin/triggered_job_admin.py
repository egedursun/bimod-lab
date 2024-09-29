#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: triggered_job_admin.py
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

from apps.mm_triggered_jobs.models import TriggeredJob


@admin.register(TriggeredJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'trigger_assistant', 'current_run_count', 'maximum_runs', 'created_at',
                    'updated_at', 'created_by_user']
    search_fields = ['name', 'trigger_assistant',
                     'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
    list_filter = ['name', 'trigger_assistant',
                   'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
