#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.urls import path

from apps.memories.views import ListAssistantMemoryView, CreateAssistantMemoryView, DeleteAssistantMemoryView

app_name = "memories"

urlpatterns = [
    path("list/", ListAssistantMemoryView.as_view(
        template_name="memories/list_memories.html"
    ), name="list"),
    path("create/", CreateAssistantMemoryView.as_view(
        template_name="memories/create_memory.html"
    ), name="create"),
    path("delete/<int:pk>/", DeleteAssistantMemoryView.as_view(),
         name="delete"),
]
