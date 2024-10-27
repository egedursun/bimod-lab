#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_board_views.py
#  Last Modified: 2024-10-26 23:43:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:43:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_core.models import LLMCore
from apps.metakanban.models import MetaKanbanBoard
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MetaKanbanView_BoardCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        context['projects'] = ProjectItem.objects.filter(organization__in=user_orgs)
        context['llm_models'] = LLMCore.objects.filter(organization__in=user_orgs)
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_METAKANBAN_BOARD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_METAKANBAN_BOARD):
            messages.error(self.request, "You do not have permission to add a kanban board.")
            return redirect('metakanban:board_list')
        ##############################

        project_id = request.POST.get("project")
        llm_model_id = request.POST.get("llm_model")
        title = request.POST.get("title")
        description = request.POST.get("description")
        if not project_id or not llm_model_id or not title:
            messages.error(request, "Please fill out all required fields.")
            return self.render_to_response(self.get_context_data())

        board = MetaKanbanBoard.objects.create(
            project_id=project_id, llm_model_id=llm_model_id, title=title,
            description=description, created_by_user=request.user,
        )
        messages.success(request, "Kanban board created successfully.")
        return redirect("metakanban:board_list")
