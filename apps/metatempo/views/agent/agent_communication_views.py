#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: agent_communication_views.py
#  Last Modified: 2024-10-28 20:46:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:46:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MetaTempoView_AgentCommunication(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - USE_METAKANBAN_AI
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.USE_METAKANBAN_AI):
            messages.error(self.request, "You do not have permission to use the AI agent for MetaTempo.")
            return redirect('metatempo:agent_communication')
        ##############################

        # TODO-EGE: Functional View: This is the view where the user will interact and ask one-shot questions to the
        #       AI agent to gather more insight about the status of the tempo within the project and the team.
        pass

        messages.success(request, f"AI agent has been successfully triggered for the selected MetaTempo connection.")
        return redirect('metatempo:agent_communication')
