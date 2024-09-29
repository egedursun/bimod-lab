#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-02 11:39:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:56:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from .views import CreateLLMCoreView, UpdateLLMCoreView, DeleteLLMCoreView, ListLLMCoreView

app_name = "llm_core"

urlpatterns = [
    path('create/', CreateLLMCoreView.as_view(template_name="llm_core/create_llm_core.html"),
         name="create"),
    path('list/', ListLLMCoreView.as_view(template_name="llm_core/list_llm_cores.html"),
         name="list"),
    path('update/<int:pk>/', UpdateLLMCoreView.as_view(template_name="llm_core/update_llm_core.html"),
         name="update"),
    path('delete/<int:pk>/', DeleteLLMCoreView.as_view(template_name="llm_core/llm_core_confirm_delete.html"),
         name="delete")
]
