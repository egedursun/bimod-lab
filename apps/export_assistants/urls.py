#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.urls import path

from apps.export_assistants.views import ListExportAssistantsView, CreateExportAssistantsView, \
    UpdateExportAssistantsView, DeleteExportAssistantsView, ExportAssistantAPIView, ToggleExportAssistantServiceView

app_name = 'export_assistants'

urlpatterns = [
    path('list/', ListExportAssistantsView.as_view(
        template_name="export_assistants/list_export_assistants.html"
    ), name='list'),
    path('create/', CreateExportAssistantsView.as_view(
        template_name="export_assistants/create_export_assistants.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateExportAssistantsView.as_view(
        template_name="export_assistants/update_export_assistants.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteExportAssistantsView.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportAssistantAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ToggleExportAssistantServiceView.as_view(), name='toggle_service'),
]
