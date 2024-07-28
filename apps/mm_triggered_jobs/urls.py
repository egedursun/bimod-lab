from django.urls import path
from .views import CreateTriggeredJobView, ListTriggeredJobsView, ListTriggeredJobLogsView, ConfirmDeleteTriggeredJobView

app_name = "mm_triggered_jobs"


urlpatterns = [
    path('create/', CreateTriggeredJobView.as_view(
        template_name='mm_triggered_jobs/create_triggered_job.html'
    ), name='create'),
    path('list/', ListTriggeredJobsView.as_view(
        template_name='mm_triggered_jobs/list_triggered_jobs.html'
    ), name='list'),
    path('logs/<int:pk>/', ListTriggeredJobLogsView.as_view(
        template_name='mm_triggered_jobs/list_triggered_job_logs.html'
    ), name='logs'),
    path('delete/<int:pk>/', ConfirmDeleteTriggeredJobView.as_view(
        template_name='mm_triggered_jobs/confirm_delete_triggered_job.html'
    ), name='delete'),
]
