#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from .views import LLMView_Create, LLMView_Update, LLMView_Delete, LLMView_List

app_name = "llm_core"

urlpatterns = [
    path('create/', LLMView_Create.as_view(template_name="llm_core/create_llm_core.html"),
         name="create"),
    path('list/', LLMView_List.as_view(template_name="llm_core/list_llm_cores.html"),
         name="list"),
    path('update/<int:pk>/', LLMView_Update.as_view(template_name="llm_core/update_llm_core.html"),
         name="update"),
    path('delete/<int:pk>/', LLMView_Delete.as_view(template_name="llm_core/llm_core_confirm_delete.html"),
         name="delete")
]
