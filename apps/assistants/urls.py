#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-12 23:24:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:19:13
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.assistants.views import CreateAssistantView, ListAssistantView, UpdateAssistantView, DeleteAssistantView

app_name = "assistants"

urlpatterns = [
    path("create/", CreateAssistantView.as_view(template_name="assistants/create_assistant.html"),
         name="create"),
    path("list/", ListAssistantView.as_view(template_name="assistants/list_assistants.html"), name="list"),
    path("update/<int:pk>/", UpdateAssistantView.as_view(template_name="assistants/update_assistant.html"),
         name="update"),
    path("delete/<int:pk>/", DeleteAssistantView.as_view(template_name="assistants/confirm_delete_assistant.html"),
         name="delete"),
]
