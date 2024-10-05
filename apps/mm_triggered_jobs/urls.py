#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-02 12:17:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:05:05
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
