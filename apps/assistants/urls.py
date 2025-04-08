#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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
from rest_framework import routers

from apps.assistants.views import (
    AssistantView_Create,
    AssistantView_List,
    AssistantView_Update,
    AssistantView_Delete,
)

app_name = "assistants"

urlpatterns = [
    path(
        "create/",
        AssistantView_Create.as_view(
            template_name="assistants/create_assistant.html"
        ),
        name="create"
    ),

    path(
        "list/",
        AssistantView_List.as_view(
            template_name="assistants/list_assistants.html"
        ),
        name="list"
    ),

    path(
        "update/<int:pk>/",
        AssistantView_Update.as_view(
            template_name="assistants/update_assistant.html"
        ),
        name="update"
    ),

    path(
        "delete/<int:pk>/",
        AssistantView_Delete.as_view(
            template_name="assistants/confirm_delete_assistant.html"
        ),
        name="delete"
    ),
]
