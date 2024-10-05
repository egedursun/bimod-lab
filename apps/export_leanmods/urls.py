#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
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
#  Last Modified: 2024-09-24 17:05:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:52:06
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.export_leanmods.views import ListExportLeanmodAssistantsView, CreateExportLeanmodAssistantsView, \
    UpdateExportLeanmodAssistantsView, DeleteExportLeanmodAssistantsView, ExportLeanmodAssistantAPIView, \
    ToggleExportLeanmodAssistantServiceView

app_name = 'export_leanmods'

urlpatterns = [
    path('list/', ListExportLeanmodAssistantsView.as_view(
        template_name="export_leanmods/list_export_leanmods.html"
    ), name='list'),
    path('create/', CreateExportLeanmodAssistantsView.as_view(
        template_name="export_leanmods/create_export_leanmods.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateExportLeanmodAssistantsView.as_view(
        template_name="export_leanmods/update_export_leanmods.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteExportLeanmodAssistantsView.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportLeanmodAssistantAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ToggleExportLeanmodAssistantServiceView.as_view(), name='toggle_service'),
]
