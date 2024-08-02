from django.urls import path
from .views import CreateTriggeredJobView, ListTriggeredJobsView, ListTriggeredJobLogsView, \
    ConfirmDeleteTriggeredJobView, TriggeredJobWebhookListenerView

app_name = "mm_triggered_jobs"

urlpatterns = [
    path('create/', CreateTriggeredJobView.as_view(
        template_name='mm_triggered_jobs/connections/create_triggered_job.html'
    ), name='create'),
    path('list/', ListTriggeredJobsView.as_view(
        template_name='mm_triggered_jobs/connections/list_triggered_jobs.html'
    ), name='list'),
    path('logs/<int:pk>/', ListTriggeredJobLogsView.as_view(
        template_name='mm_triggered_jobs/logs/list_triggered_job_logs.html'
    ), name='logs'),
    path('delete/<int:pk>/', ConfirmDeleteTriggeredJobView.as_view(
        template_name='mm_triggered_jobs/connections/confirm_delete_triggered_job.html'
    ), name='delete'),

    path('api/v1/webhook/<str:assistant_id>/<int:triggered_job_id>/', TriggeredJobWebhookListenerView.as_view(),
         name='webhook'),
]
