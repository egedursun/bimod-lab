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

from apps.mm_triggered_jobs.models import TriggeredJobInstance


@admin.register(TriggeredJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = ['triggered_job', 'status', 'started_at', 'ended_at']
    search_fields = ['triggered_job', 'status', 'started_at', 'ended_at']
    list_filter = ['triggered_job', 'status', 'started_at', 'ended_at']
