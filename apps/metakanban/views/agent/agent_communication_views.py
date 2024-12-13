#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: agent_communication_views.py
#  Last Modified: 2024-10-27 18:54:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 18:54:43
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.core.metakanban.metakanban_execution_handler import (
    MetaKanbanExecutionManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import (
    MetaKanbanBoard
)

from apps.organization.models import Organization
from apps.projects.models import ProjectItem

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MetaKanbanView_AgentCommunication(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        organization_projects = ProjectItem.objects.filter(
            organization__in=user_orgs
        )

        organization_boards = MetaKanbanBoard.objects.filter(
            project__in=organization_projects
        )

        context['organization_boards'] = organization_boards

        return context

    def post(self, request, *args, **kwargs):
        board_id = request.POST.get('board_id')

        ##############################
        # PERMISSION CHECK FOR - USE_METAKANBAN_AI
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.USE_METAKANBAN_AI
        ):
            messages.error(self.request, "You do not have permission to use MetaKanban AI.")
            return redirect('metakanban:agent_communication')
        ##############################

        user_query = request.POST.get('user_query')

        try:
            xc = MetaKanbanExecutionManager(
                board_id=board_id
            )

            success, llm_output = xc.consult_ai(
                user_query=user_query
            )

            if not success:
                messages.error(request, "Error executing MetaKanban query.")

                return redirect('metakanban:agent_communication')

        except Exception as e:
            messages.error(request, f"Error executing MetaKanban query: {e}")

            return redirect('metakanban:agent_communication')

        context = self.get_context_data()

        context.update(
            {
                "llm_output": llm_output,
            }
        )

        messages.success(request, "MetaKanban query executed successfully.")

        return render(request, 'metakanban/agent/agent_communication.html', context)
