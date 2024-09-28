#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.


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
