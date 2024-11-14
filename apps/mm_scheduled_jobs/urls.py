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
from .views.log.list_orchestration_scheduled_job_logs_views import ScheduledJobView_OrchestrationLogList
from .views.scheduled_job.create_orchestration_scheduled_job_views import ScheduledJobView_OrchestrationCreate
from .views.scheduled_job.delete_orchestration_scheduled_jobs_views import ScheduledJobView_OrchestrationDelete
from .views.scheduled_job.list_orchestration_scheduled_jobs_views import ScheduledJobView_OrchestrationList

app_name = "mm_scheduled_jobs"

urlpatterns = [
    path('create/', ScheduledJobView_Create.as_view(template_name='mm_scheduled_jobs/create_scheduled_job.html'),
         name='create'),
    path('list/', ScheduledJobView_List.as_view(template_name='mm_scheduled_jobs/list_scheduled_jobs.html'),
         name='list'),
    path('logs/<int:pk>/', ScheduledJobView_LogList.as_view(
        template_name='mm_scheduled_jobs/list_scheduled_job_logs.html'), name='logs'),
    path('confirm-delete/<int:pk>/', ScheduledJobView_Delete.as_view(
        template_name='mm_scheduled_jobs/confirm_delete_scheduled_job.html'), name='delete'),

    #####

    path('orchestration/create/', ScheduledJobView_OrchestrationCreate.as_view(
        template_name='mm_scheduled_jobs/create_orchestration_scheduled_job.html'), name='orchestration_create'),
    path('orchestration/list/', ScheduledJobView_OrchestrationList.as_view(
        template_name='mm_scheduled_jobs/list_orchestration_scheduled_jobs.html'), name='orchestration_list'),
    path('orchestration/logs/<int:pk>/', ScheduledJobView_OrchestrationLogList.as_view(
        template_name='mm_scheduled_jobs/list_orchestration_scheduled_job_logs.html'), name='orchestration_logs'),
    path('orchestration/confirm-delete/<int:pk>/', ScheduledJobView_OrchestrationDelete.as_view(
        template_name='mm_scheduled_jobs/confirm_delete_orchestration_scheduled_job.html'), name='orchestration_delete'),
]
