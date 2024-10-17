#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from .views import (ExportOrchestrationView_List, ExportOrchestrationView_Create, ExportOrchestrationView_Update,
                    ExportOrchestrationView_Delete, ExportOrchestrationAPIView, ExportOrchestrationView_ToggleService)

app_name = 'export_orchestrations'

urlpatterns = [
    path('list/', ExportOrchestrationView_List.as_view(
        template_name="export_orchestrations/list_export_orchestrations.html"), name='list'),
    path('create/', ExportOrchestrationView_Create.as_view(
        template_name="export_orchestrations/create_export_orchestrations.html"), name='create'),
    path('update/<int:pk>/', ExportOrchestrationView_Update.as_view(
        template_name="export_orchestrations/update_export_orchestrations.html"), name='update'),
    path('delete/<int:pk>/', ExportOrchestrationView_Delete.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportOrchestrationAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ExportOrchestrationView_ToggleService.as_view(), name='toggle_service'),
]
