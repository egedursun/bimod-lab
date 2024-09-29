#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-09-24 19:12:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:53:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from .views import (ListExportOrchestrationsView, CreateExportOrchestrationView, UpdateExportOrchestrationView,
                    DeleteExportOrchestrationView, ExportOrchestrationAPIView, ToggleExportOrchestrationServiceView)

app_name = 'export_orchestrations'

urlpatterns = [
    path('list/', ListExportOrchestrationsView.as_view(
        template_name="export_orchestrations/list_export_orchestrations.html"
    ), name='list'),
    path('create/', CreateExportOrchestrationView.as_view(
        template_name="export_orchestrations/create_export_orchestrations.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateExportOrchestrationView.as_view(
        template_name="export_orchestrations/update_export_orchestrations.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteExportOrchestrationView.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportOrchestrationAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ToggleExportOrchestrationServiceView.as_view(), name='toggle_service'),
]
