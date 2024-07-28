from django.urls import path

from .views import (CreateScheduledJobView, ListScheduledJobsView, ListScheduledJobLogsView,
                    ConfirmDeleteScheduledJobView)

app_name = "mm_scheduled_jobs"

urlpatterns = [
    path('create/', CreateScheduledJobView.as_view(
        template_name='mm_scheduled_jobs/create_scheduled_job.html'
    ), name='create'),
    path('list/', ListScheduledJobsView.as_view(
        template_name='mm_scheduled_jobs/list_scheduled_jobs.html'
    ), name='list'),
    path('logs/', ListScheduledJobLogsView.as_view(
        template_name='mm_scheduled_jobs/list_scheduled_job_logs.html'
    ), name='logs'),
    path('confirm-delete/', ConfirmDeleteScheduledJobView.as_view(
        template_name='mm_scheduled_jobs/confirm_delete_scheduled_job.html'
    ), name='delete'),
]
