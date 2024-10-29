#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_metatempo_connection_views.py
#  Last Modified: 2024-10-28 20:29:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:29:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.metakanban.models import MetaKanbanBoard
from apps.metatempo.models import MetaTempoConnection
from apps.metatempo.utils import METATEMPO_MEMBER_LOG_INTERVALS, METATEMPO_OVERALL_LOG_INTERVALS, \
    META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from web_project import TemplateLayout


class MetaTempoView_ConnectionCreate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        user_projects = ProjectItem.objects.filter(organization__in=user_orgs)
        context['boards'] = MetaKanbanBoard.objects.filter(project__in=user_projects)
        context['METATEMPO_OVERALL_LOG_INTERVALS'] = METATEMPO_OVERALL_LOG_INTERVALS
        context['METATEMPO_MEMBER_LOG_INTERVALS'] = METATEMPO_MEMBER_LOG_INTERVALS
        return context

    def post(self, request, *args, **kwargs):
        board_id = request.POST.get("board")
        is_tracking_active = request.POST.get("is_tracking_active") == "True"
        overall_log_intervals = request.POST.get("overall_log_intervals")
        member_log_intervals = request.POST.get("member_log_intervals")
        tracked_weekdays = request.POST.getlist("tracked_weekdays")
        tracking_start_time = request.POST.get("tracking_start_time")
        tracking_end_time = request.POST.get("tracking_end_time")
        connection_api_key = str(secrets.token_urlsafe(META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH))
        optional_context_instructions = request.POST.get("optional_context_instructions")

        board = MetaKanbanBoard.objects.get(id=board_id)

        MetaTempoConnection.objects.create(
            board=board,
            is_tracking_active=is_tracking_active,
            overall_log_intervals=overall_log_intervals,
            member_log_intervals=member_log_intervals,
            tracked_weekdays=tracked_weekdays,
            tracking_start_time=tracking_start_time,
            tracking_end_time=tracking_end_time,
            connection_api_key=connection_api_key,
            created_by_user=request.user,
            optional_context_instructions=optional_context_instructions
        )

        messages.success(request, "MetaTempo Connection created successfully.")
        return redirect("metatempo:connection_list")
