#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_hadron_node_views.py
#  Last Modified: 2024-10-17 22:51:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:51:25
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

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.hadron_prime.models import HadronNode, HadronTopic, HadronSystem
from apps.llm_core.models import LLMCore
from apps.leanmod.models import ExpertNetwork
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_UpdateHadronNode(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        systems = HadronSystem.objects.filter(organization__in=user_orgs)
        llm_models = LLMCore.objects.filter(organization__in=user_orgs)
        expert_networks = ExpertNetwork.objects.filter(organization__in=user_orgs)
        topics = HadronTopic.objects.filter(system__organization__in=user_orgs)
        node = get_object_or_404(HadronNode, pk=self.kwargs['pk'])
        selected_topic_ids = list(node.subscribed_topics.values_list('id', flat=True))
        selected_expert_network_ids = list(node.expert_networks.values_list('id', flat=True))

        context['node'] = node
        context['systems'] = systems
        context['llm_models'] = llm_models
        context['expert_networks'] = expert_networks
        context['topics'] = topics
        context['selected_topic_ids'] = selected_topic_ids
        context['selected_expert_network_ids'] = selected_expert_network_ids
        return context

    def post(self, request, *args, **kwargs):
        node = get_object_or_404(HadronNode, pk=self.kwargs['pk'])
        system_id = request.POST.get('system')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_HADRON_NODES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_HADRON_NODES):
            messages.error(self.request, "You do not have permission to update Hadron Nodes.")
            return redirect('hadron_prime:detail_hadron_system', pk=node.system_id)
        ##############################

        llm_model_id = request.POST.get('llm_model')
        node_name = request.POST.get('node_name')
        node_description = request.POST.get('node_description')
        optional_instructions = request.POST.get('optional_instructions')

        # Retrieve Current State fields
        current_state_curl = request.POST.get('current_state_curl')
        current_state_input_desc = request.POST.get('current_state_input_params_description')
        current_state_output_desc = request.POST.get('current_state_output_params_description')
        # Retrieve Goal State fields
        goal_state_curl = request.POST.get('goal_state_curl')
        goal_state_input_desc = request.POST.get('goal_state_input_params_description')
        goal_state_output_desc = request.POST.get('goal_state_output_params_description')
        # Retrieve error calculation
        error_calculation_curl = request.POST.get('error_calculation_curl')
        error_calculation_input_desc = request.POST.get('error_calculation_input_params_description')
        error_calculation_output_desc = request.POST.get('error_calculation_output_params_description')
        # Retrieve Sensory Measurements fields
        measurements_curl = request.POST.get('measurements_curl')
        measurements_input_desc = request.POST.get('measurements_input_params_description')
        measurements_output_desc = request.POST.get('measurements_output_params_description')
        # Retrieve Action Set fields
        action_set_curl = request.POST.get('action_set_curl')
        action_set_input_desc = request.POST.get('action_set_input_params_description')
        action_set_output_desc = request.POST.get('action_set_output_params_description')
        # Retrieve Analytic Calculation fields
        analytic_calculation_curl = request.POST.get('analytic_calculation_curl')
        analytic_calculation_input_desc = request.POST.get('analytic_calculation_input_params_description')
        analytic_calculation_output_desc = request.POST.get('analytic_calculation_output_params_description')
        # Retrieve Actuation fields
        actuation_curl = request.POST.get('actuation_curl')
        actuation_input_desc = request.POST.get('actuation_input_params_description')
        actuation_output_desc = request.POST.get('actuation_output_params_description')
        # Additional fields if required for relations:
        subscribed_topics = request.POST.getlist('subscribed_topics')
        expert_networks = request.POST.getlist('expert_networks')
        # Lookback memory sizes
        state_action_state_lookback_memory_size = request.POST.get('state_action_state_lookback_memory_size')
        publishing_history_lookback_memory_size = request.POST.get('publishing_history_lookback_memory_size')
        topic_messages_history_lookback_memory_size = request.POST.get('topic_messages_history_lookback_memory_size')

        # Update the node object
        node.system_id = system_id
        node.llm_model_id = llm_model_id
        node.node_name = node_name
        node.node_description = node_description
        node.optional_instructions = optional_instructions
        node.current_state_curl = current_state_curl
        node.current_state_input_params_description = current_state_input_desc
        node.current_state_output_params_description = current_state_output_desc
        node.goal_state_curl = goal_state_curl
        node.goal_state_input_params_description = goal_state_input_desc
        node.goal_state_output_params_description = goal_state_output_desc
        node.error_calculation_curl = error_calculation_curl
        node.error_calculation_input_params_description = error_calculation_input_desc
        node.error_calculation_output_params_description = error_calculation_output_desc
        node.measurements_curl = measurements_curl
        node.measurements_input_params_description = measurements_input_desc
        node.measurements_output_params_description = measurements_output_desc
        node.action_set_curl = action_set_curl
        node.action_set_input_params_description = action_set_input_desc
        node.action_set_output_params_description = action_set_output_desc
        node.analytic_calculation_curl = analytic_calculation_curl
        node.analytic_calculation_input_params_description = analytic_calculation_input_desc
        node.analytic_calculation_output_params_description = analytic_calculation_output_desc
        node.actuation_curl = actuation_curl
        node.actuation_input_params_description = actuation_input_desc
        node.actuation_output_params_description = actuation_output_desc
        node.state_action_state_lookback_memory_size = state_action_state_lookback_memory_size
        node.publishing_history_lookback_memory_size = publishing_history_lookback_memory_size
        node.topic_messages_history_lookback_memory_size = topic_messages_history_lookback_memory_size

        node.save()
        node.subscribed_topics.set(subscribed_topics)
        node.expert_networks.set(expert_networks)

        logger.info(f'Node updated: {node}')
        messages.success(request, 'Node updated successfully.')
        return redirect('hadron_prime:detail_hadron_node', pk=node.id)
