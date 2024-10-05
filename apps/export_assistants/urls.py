#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
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
#  Last Modified: 2024-08-02 11:30:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:50:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
