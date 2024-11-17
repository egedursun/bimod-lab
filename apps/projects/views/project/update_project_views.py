#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_project_views.py
#  Last Modified: 2024-10-24 22:02:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:02:04
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

from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ProjectsView_ProjectUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        project_id = self.kwargs.get("pk")
        project = get_object_or_404(ProjectItem, pk=project_id)
        context['project'] = project
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs.get("pk")
        project = get_object_or_404(ProjectItem, pk=project_id)

        try:
            project.organization_id = request.POST.get('organization')
            project.project_name = request.POST.get('project_name')
            project.project_department = request.POST.get('project_department')
            project.project_description = request.POST.get('project_description')
            project.project_status = request.POST.get('project_status')
            project.project_priority = request.POST.get('project_priority')
            project.project_risk_level = request.POST.get('project_risk_level')
            project.project_goals = request.POST.get('project_goals')
            project.project_constraints = request.POST.get('project_constraints')
            project.project_stakeholders = request.POST.get('project_stakeholders')
            project.project_start_date = request.POST.get('project_start_date')
            project.project_end_date = request.POST.get('project_end_date')
            project.project_budget = request.POST.get('project_budget')

            project.save()
        except Exception as e:
            messages.error(request, f"An error occurred while updating the Project: {str(e)}")
            return redirect("projects:project_list")

        messages.success(request, "Project updated successfully!")
        logger.info(f"Project updated successfully: {project.id}")
        return redirect('projects:project_list')
