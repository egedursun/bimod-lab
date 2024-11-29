#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-24 20:05:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 20:05:10
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from apps.export_voidforger.views import (
    ExportVoidForgerView_List,
    ExportVoidForgerView_Create,
    ExportVoidForgerView_Update,
    ExportVoidForgerView_Delete,
    ExportVoidForgerAPIView,
    ExportVoidForgerAPIHealthCheckView,
    ExportVoidForgerView_ToggleService,
    ExportVoidForgerAPIStatusView,
    ExportVoidForgerAPIManualTriggerView,
)

app_name = "export_voidforger"

urlpatterns = [
    path(
        'list/',
        ExportVoidForgerView_List.as_view(
            template_name="export_voidforger/list_export_voidforger.html"
        ),
        name='list'
    ),

    path(
        'create/',
        ExportVoidForgerView_Create.as_view(
            template_name="export_voidforger/create_export_voidforger.html"
        ),
        name='create'
    ),

    path(
        'update/<int:pk>/',
        ExportVoidForgerView_Update.as_view(
            template_name="export_voidforger/update_export_voidforger.html"
        ),
        name='update'
    ),

    path(
        'delete/<int:pk>/',
        ExportVoidForgerView_Delete.as_view(

        ),
        name='delete'
    ),

    path(
        'exported/voidforger_assistants/<int:organization_id>/<int:assistant_id>/<int:export_id>/',
        ExportVoidForgerAPIView.as_view(

        ),
        name='api'
    ),

    path(
        'health/voidforger_assistants/<int:organization_id>/<int:assistant_id>/<int:export_id>/',
        ExportVoidForgerAPIHealthCheckView.as_view(

        ),
        name='health_check'
    ),

    path(
        'toggle_service/<int:pk>/',
        ExportVoidForgerView_ToggleService.as_view(),
        name='toggle_service'
    ),

    path(
        'status/voidforger_assistants/<int:organization_id>/<int:assistant_id>/<int:export_id>/',
        ExportVoidForgerAPIStatusView.as_view(),
        name='status'
    ),

    path(
        'manual_trigger/<int:pk>/',
        ExportVoidForgerAPIManualTriggerView.as_view(),
        name='manual_trigger'
    ),
]
