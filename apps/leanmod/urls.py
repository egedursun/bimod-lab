#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:31
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
#  Last Modified: 2024-09-23 12:33:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:55:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.leanmod.views import CreateLeanAssistantView, UpdateLeanAssistantView, DeleteLeanAssistantView, \
    ListLeanAssistantsView, CreateExpertNetworkView, UpdateExpertNetworkView, DeleteExpertNetworkView, \
    ListExpertNetworksView

app_name = 'leanmod'

urlpatterns = [
    path('create/', CreateLeanAssistantView.as_view(
        template_name="leanmod/lean_assistant/create_lean_assistant.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateLeanAssistantView.as_view(
        template_name="leanmod/lean_assistant/update_lean_assistant.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteLeanAssistantView.as_view(
        template_name="leanmod/lean_assistant/confirm_delete_lean_assistant.html"
    ), name='delete'),
    path('list/', ListLeanAssistantsView.as_view(
        template_name="leanmod/lean_assistant/list_lean_assistants.html"
    ), name='list'),
    #####
    path('create_expert_network/', CreateExpertNetworkView.as_view(
        template_name="leanmod/expert_network/create_expert_network.html"
    ), name='create_expert_network'),
    path('update_expert_network/<int:pk>/', UpdateExpertNetworkView.as_view(
        template_name="leanmod/expert_network/update_expert_network.html"
    ), name='update_expert_network'),
    path('delete_expert_network/<int:pk>/', DeleteExpertNetworkView.as_view(
        template_name="leanmod/expert_network/confirm_delete_expert_network.html"
    ), name='delete_expert_network'),
    path('list_expert_network/', ListExpertNetworksView.as_view(
        template_name="leanmod/expert_network/list_expert_networks.html"
    ), name='list_expert_networks'),
]
