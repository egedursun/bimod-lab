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

from .views import (ScheduledJobView_Create, ScheduledJobView_List, ScheduledJobView_LogList,
                    ScheduledJobView_Delete)

app_name = "mm_scheduled_jobs"

urlpatterns = [
    path('create/', ScheduledJobView_Create.as_view(template_name='mm_scheduled_jobs/create_scheduled_job.html'),
         name='create'),
    path('list/', ScheduledJobView_List.as_view(template_name='mm_scheduled_jobs/list_scheduled_jobs.html'),
         name='list'),
    path('logs/<int:pk>/', ScheduledJobView_LogList.as_view(
        template_name='mm_scheduled_jobs/list_scheduled_job_logs.html'), name='logs'),
    path('confirm-delete/<int:pk>', ScheduledJobView_Delete.as_view(
        template_name='mm_scheduled_jobs/confirm_delete_scheduled_job.html'), name='delete'),
]
