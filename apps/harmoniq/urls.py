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

from apps.harmoniq.views import (ListHarmoniqAgentsView, UseHarmoniqAgentView, CreateHarmoniqAgentView,
                                 UpdateHarmoniqAgentView, ConfirmDeleteHarmoniqAgentView)

app_name = 'harmoniq'

urlpatterns = [
    path("use/<int:pk>/", UseHarmoniqAgentView.as_view(
        template_name="harmoniq/use_harmoniq_agent.html"), name="use"),
    path("list/", ListHarmoniqAgentsView.as_view(
        template_name="harmoniq/list_harmoniq_agents.html"), name="list"),
    path("create/", CreateHarmoniqAgentView.as_view(
        template_name="harmoniq/create_harmoniq_agent.html"), name="create"),
    path("update/<int:pk>/", UpdateHarmoniqAgentView.as_view(
        template_name="harmoniq/update_harmoniq_agent.html"), name="update"),
    path("delete/<int:pk>/", ConfirmDeleteHarmoniqAgentView.as_view(
        template_name="harmoniq/confirm_delete_harmoniq_agent.html"), name="confirm_delete"),
]
