#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.urls import path
from .views import TriggeredJobView_Create, TriggeredJobView_List, TriggeredJobView_LogList, \
    TriggeredJobView_Delete, TriggeredJobWebhookListenerView, TriggeredJobView_OrchestrationCreate, \
    TriggeredJobView_OrchestrationList, TriggeredJobView_OrchestrationLogList, TriggeredJobView_OrchestrationDelete, \
    OrchestrationTriggeredJobWebhookListenerView

app_name = "mm_triggered_jobs"

urlpatterns = [
    path('create/', TriggeredJobView_Create.as_view(
        template_name='mm_triggered_jobs/connections/create_triggered_job.html'), name='create'),
    path('list/', TriggeredJobView_List.as_view(
        template_name='mm_triggered_jobs/connections/list_triggered_jobs.html'), name='list'),
    path('logs/<int:pk>/', TriggeredJobView_LogList.as_view(
        template_name='mm_triggered_jobs/logs/list_triggered_job_logs.html'), name='logs'),
    path('delete/<int:pk>/', TriggeredJobView_Delete.as_view(
        template_name='mm_triggered_jobs/connections/confirm_delete_triggered_job.html'), name='delete'),
    path('api/v1/webhook/<str:assistant_id>/<int:triggered_job_id>/', TriggeredJobWebhookListenerView.as_view(),
         name='webhook'),

    #####

    path('orchestration/create/', TriggeredJobView_OrchestrationCreate.as_view(
        template_name='mm_triggered_jobs/connections/orchestration_create_triggered_job.html'), name='orchestration_create'),
    path('orchestration/list/', TriggeredJobView_OrchestrationList.as_view(
        template_name='mm_triggered_jobs/connections/orchestration_list_triggered_jobs.html'), name='orchestration_list'),
    path('orchestration/logs/<int:pk>/', TriggeredJobView_OrchestrationLogList.as_view(
        template_name='mm_triggered_jobs/logs/orchestration_list_triggered_job_logs.html'), name='orchestration_logs'),
    path('orchestration/delete/<int:pk>/', TriggeredJobView_OrchestrationDelete.as_view(
        template_name='mm_triggered_jobs/connections/orchestration_confirm_delete_triggered_job.html'), name='orchestration_delete'),
    path('orchestration/api/v1/webhook/<str:maestro_id>/<int:triggered_job_id>/', OrchestrationTriggeredJobWebhookListenerView.as_view(),
         name='orchestration_webhook'),
]
