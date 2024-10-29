#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_metatempo_connection_views.py
#  Last Modified: 2024-10-28 20:29:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:29:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.metakanban.models import MetaKanbanBoard
from apps.metatempo.models import MetaTempoConnection
from apps.metatempo.utils import METATEMPO_OVERALL_LOG_INTERVALS, METATEMPO_MEMBER_LOG_INTERVALS
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from web_project import TemplateLayout

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView


class MetaTempoView_ConnectionUpdate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        connection_id = kwargs['connection_id']
        connection = get_object_or_404(MetaTempoConnection, id=connection_id)

        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        user_projects = ProjectItem.objects.filter(organization__in=user_orgs)

        context.update({
            'connection': connection,
            'boards': MetaKanbanBoard.objects.filter(project__in=user_projects),
            'METATEMPO_OVERALL_LOG_INTERVALS': METATEMPO_OVERALL_LOG_INTERVALS,
            'METATEMPO_MEMBER_LOG_INTERVALS': METATEMPO_MEMBER_LOG_INTERVALS,
        })
        return context

    def post(self, request, *args, **kwargs):
        connection_id = kwargs['connection_id']
        connection = get_object_or_404(MetaTempoConnection, id=connection_id)

        board_id = request.POST.get("board")
        is_tracking_active = request.POST.get("is_tracking_active") == "True"
        overall_log_intervals = request.POST.get("overall_log_intervals")
        member_log_intervals = request.POST.get("member_log_intervals")
        tracked_weekdays = request.POST.getlist("tracked_weekdays")
        tracking_start_time = request.POST.get("tracking_start_time")
        tracking_end_time = request.POST.get("tracking_end_time")
        optional_context_instructions = request.POST.get("optional_context_instructions")

        connection.board = MetaKanbanBoard.objects.get(id=board_id)
        connection.is_tracking_active = is_tracking_active
        connection.overall_log_intervals = overall_log_intervals
        connection.member_log_intervals = member_log_intervals
        connection.tracked_weekdays = tracked_weekdays
        connection.tracking_start_time = tracking_start_time
        connection.tracking_end_time = tracking_end_time
        connection.optional_context_instructions = optional_context_instructions
        connection.save()

        messages.success(request, "MetaTempo Connection updated successfully.")
        return redirect("metatempo:connection_list")
