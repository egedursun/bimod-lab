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
#  Last Modified: 2024-07-28 09:22:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:02:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
    path('logs/<int:pk>/', ListScheduledJobLogsView.as_view(
        template_name='mm_scheduled_jobs/list_scheduled_job_logs.html'
    ), name='logs'),
    path('confirm-delete/<int:pk>', ConfirmDeleteScheduledJobView.as_view(
        template_name='mm_scheduled_jobs/confirm_delete_scheduled_job.html'
    ), name='delete'),
]
