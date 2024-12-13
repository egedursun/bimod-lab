#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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

from apps.leanmod.views import (
    LeanModAssistantView_Create,
    LeanModAssistantView_Update,
    LeanModAssistantView_Delete,
    LeanModAssistantView_List,
    ExpertNetworkView_Create,
    ExpertNetworkView_Update,
    ExpertNetworkView_Delete,
    ExpertNetworkView_List
)

app_name = 'leanmod'

urlpatterns = [
    path(
        'create/',
        LeanModAssistantView_Create.as_view(
            template_name="leanmod/lean_assistant/create_lean_assistant.html"
        ),
        name='create'
    ),
    path(
        'update/<int:pk>/',
        LeanModAssistantView_Update.as_view(
            template_name="leanmod/lean_assistant/update_lean_assistant.html"
        ),
        name='update'
    ),
    path(
        'delete/<int:pk>/',
        LeanModAssistantView_Delete.as_view(
            template_name="leanmod/lean_assistant/confirm_delete_lean_assistant.html"
        ),
        name='delete'
    ),
    path(
        'list/',
        LeanModAssistantView_List.as_view(
            template_name="leanmod/lean_assistant/list_lean_assistants.html"
        ),
        name='list'
    ),

    #####

    path(
        'create_expert_network/',
        ExpertNetworkView_Create.as_view(
            template_name="leanmod/expert_network/create_expert_network.html"
        ),
        name='create_expert_network'
    ),

    path(
        'update_expert_network/<int:pk>/',
        ExpertNetworkView_Update.as_view(
            template_name="leanmod/expert_network/update_expert_network.html"
        ),
        name='update_expert_network'
    ),

    path(
        'delete_expert_network/<int:pk>/',
        ExpertNetworkView_Delete.as_view(
            template_name="leanmod/expert_network/confirm_delete_expert_network.html"
        ),
        name='delete_expert_network'
    ),

    path(
        'list_expert_network/',
        ExpertNetworkView_List.as_view(
            template_name="leanmod/expert_network/list_expert_networks.html"
        ),
        name='list_expert_networks'
    ),
]
