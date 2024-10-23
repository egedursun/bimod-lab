#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_hadron_node_views.py
#  Last Modified: 2024-10-18 00:24:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 00:24:17
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
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.hadron_prime.models import HadronNode
from apps.user_permissions.utils import PermissionNames
from config.settings import BASE_URL
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_DetailHadronNode(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_HADRON_NODES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_HADRON_NODES):
            messages.error(self.request, "You do not have permission to list Hadron Nodes.")
            return context
        ##############################

        node = get_object_or_404(HadronNode, id=kwargs['pk'])
        context['node'] = node

        # Fetch speech logs
        speech_logs = node.speech_logs.all().order_by('-created_at')
        paginator_speech_logs = Paginator(speech_logs, 10)
        page_number_speech_logs = self.request.GET.get('speech_logs_page')
        context['speech_logs_page_obj'] = paginator_speech_logs.get_page(page_number_speech_logs)
        # Fetch execution logs
        execution_logs = node.execution_logs.all().order_by('-created_at')
        paginator_exec_logs = Paginator(execution_logs, 10)
        page_number_exec_logs = self.request.GET.get('execution_logs_page')
        context['execution_logs_page_obj'] = paginator_exec_logs.get_page(page_number_exec_logs)
        # Fetch state-error-action-state-error logs
        seas_logs = node.state_action_state_history_logs.all().order_by('-created_at')
        paginator_seas_logs = Paginator(seas_logs, 10)
        page_number_seas_logs = self.request.GET.get('seas_logs_page')
        context['seas_logs_page_obj'] = paginator_seas_logs.get_page(page_number_seas_logs)
        # Fetch publishing logs (HadronTopicMessages)
        topic_messages = node.publishing_history_logs.all().order_by('-created_at')
        paginator_topic_logs = Paginator(topic_messages, 10)
        page_number_topic_logs = self.request.GET.get('publishing_logs_page')
        context['publishing_logs_page_obj'] = paginator_topic_logs.get_page(page_number_topic_logs)
        context["BASE_URL"] = BASE_URL
        return context
