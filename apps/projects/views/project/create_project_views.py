#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_project_views.py
#  Last Modified: 2024-10-24 22:01:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:01:57
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ProjectsView_ProjectCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user
        org_id = request.POST.get('organization')
        project_name = request.POST.get('project_name')
        project_department = request.POST.get('project_department')
        project_description = request.POST.get('project_description')
        project_status = request.POST.get('project_status')
        project_priority = request.POST.get('project_priority')
        project_risk_level = request.POST.get('project_risk_level')
        project_goals = request.POST.get('project_goals')
        project_constraints = request.POST.get('project_constraints')
        project_stakeholders = request.POST.get('project_stakeholders')
        project_start_date = request.POST.get('project_start_date')
        project_end_date = request.POST.get('project_end_date')
        project_budget = request.POST.get('project_budget')

        if not (org_id and project_name and project_department and project_description):
            messages.error(request, "Required fields are missing.")
            return redirect('projects:project_create')

        org = Organization.objects.get(id=org_id)

        try:
            project_item = ProjectItem.objects.create(
                organization=org, project_name=project_name, project_department=project_department,
                project_description=project_description, project_status=project_status,
                project_priority=project_priority, project_risk_level=project_risk_level,
                project_goals=project_goals, project_constraints=project_constraints,
                project_stakeholders=project_stakeholders, project_start_date=project_start_date,
                project_end_date=project_end_date, project_budget=project_budget,
                created_by_user=context_user
            )
        except Exception as e:
            messages.error(request, "Project creation failed.")
            logger.error(f"Project creation failed: {e}")
            return redirect('projects:project_create')

        messages.success(request, "Project created successfully.")
        logger.info(f"Project created successfully: {project_item.id}")
        return redirect('projects:project_list')
