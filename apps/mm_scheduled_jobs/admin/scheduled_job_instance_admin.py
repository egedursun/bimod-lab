from django.contrib import admin

from apps.mm_scheduled_jobs.models import ScheduledJobInstance


@admin.register(ScheduledJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = ['scheduled_job', 'status', 'started_at', 'ended_at']
    search_fields = ['scheduled_job', 'status', 'started_at', 'ended_at']
    list_filter = ['scheduled_job', 'status', 'started_at', 'ended_at']
