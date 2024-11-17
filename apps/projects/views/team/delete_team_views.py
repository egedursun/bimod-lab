#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_team_views.py
#  Last Modified: 2024-10-24 22:02:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:02:27
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

from apps.projects.models import ProjectTeamItem
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ProjectsView_TeamDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        team_id = self.kwargs.get('pk')
        team = get_object_or_404(ProjectTeamItem, pk=team_id)
        context['team'] = team
        return context

    def post(self, request, *args, **kwargs):
        team_id = self.kwargs.get('pk')
        team = get_object_or_404(ProjectTeamItem, pk=team_id)
        team_name = team.team_name

        try:
            team.delete()
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the Team: {str(e)}')
            return redirect('projects:team_list')

        messages.success(request, f'Team "{team_name}" has been successfully deleted.')
        logger.info(f'Team deleted: {team_name}')
        return redirect('projects:team_list')
