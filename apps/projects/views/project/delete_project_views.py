#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_project_views.py
#  Last Modified: 2024-10-24 22:02:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:02:10
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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.projects.models import ProjectItem
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ProjectsView_ProjectDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        project_id = self.kwargs.get("pk")
        context['project'] = get_object_or_404(ProjectItem, pk=project_id)
        return context

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs.get("pk")
        project = get_object_or_404(ProjectItem, pk=project_id)

        try:
            project.delete()
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the Project: {str(e)}")
            return redirect("projects:project_list")

        messages.success(request, f"Project '{project.project_name}' has been deleted successfully.")
        logger.info(f"Project deleted: {project_id}")
        return redirect('projects:project_list')
