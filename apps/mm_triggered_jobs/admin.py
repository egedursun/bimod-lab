from django.contrib import admin

from apps.mm_triggered_jobs.models import TriggeredJob, TriggeredJobInstance


# Register your models here.


@admin.register(TriggeredJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'trigger_assistant',
                    'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
    search_fields = ['name', 'trigger_assistant',
                     'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
    list_filter = ['name', 'trigger_assistant',
                   'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']


@admin.register(TriggeredJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = ['triggered_job', 'status', 'started_at', 'ended_at']
    search_fields = ['triggered_job', 'status', 'started_at', 'ended_at']
    list_filter = ['triggered_job', 'status', 'started_at', 'ended_at']
