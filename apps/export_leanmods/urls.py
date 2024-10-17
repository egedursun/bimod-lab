#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.export_leanmods.views import ExportLeanModView_List, ExportLeanModView_Create, \
    ExportLeanModView_Update, ExportLeanModView_Delete, ExportLeanmodAssistantAPIView, \
    ExportLeanModView_ToggleService

app_name = 'export_leanmods'

urlpatterns = [
    path('list/', ExportLeanModView_List.as_view(
        template_name="export_leanmods/list_export_leanmods.html"), name='list'),
    path('create/', ExportLeanModView_Create.as_view(
        template_name="export_leanmods/create_export_leanmods.html"), name='create'),
    path('update/<int:pk>/', ExportLeanModView_Update.as_view(
        template_name="export_leanmods/update_export_leanmods.html"), name='update'),
    path('delete/<int:pk>/', ExportLeanModView_Delete.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportLeanmodAssistantAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ExportLeanModView_ToggleService.as_view(), name='toggle_service'),
]
