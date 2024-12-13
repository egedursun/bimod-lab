#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_hadron_node_views.py
#  Last Modified: 2024-10-17 22:51:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:51:19
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.hadron_prime.models import (
    HadronSystem,
    HadronNode,
    HadronTopic
)

from apps.leanmod.models import ExpertNetwork
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_CreateHadronNode(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        systems = HadronSystem.objects.filter(
            organization__in=user_orgs
        )

        llm_models = LLMCore.objects.filter(
            organization__in=user_orgs
        )

        expert_networks = ExpertNetwork.objects.filter(
            organization__in=user_orgs
        )

        topics = HadronTopic.objects.filter(
            system__organization__in=user_orgs
        )

        context['organizations'] = user_orgs
        context['systems'] = systems
        context['llm_models'] = llm_models
        context['expert_networks'] = expert_networks
        context['topics'] = topics

        return context

    def post(self, request, *args, **kwargs):
        # Get data from POST request
        system_id = request.POST.get('system')

        ##############################
        # PERMISSION CHECK FOR - CREATE_HADRON_NODES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CREATE_HADRON_NODES
        ):
            messages.error(self.request, "You do not have permission to create Hadron Nodes.")
            return redirect(
                'hadron_prime:detail_hadron_system',
                pk=system_id
            )
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

        try:

            # Create the HadronNode object

            node = HadronNode.objects.create(
                system_id=system_id,
                llm_model_id=llm_model_id,
                node_name=node_name,
                node_description=node_description,
                optional_instructions=optional_instructions,
                current_state_curl=current_state_curl,
                current_state_input_params_description=current_state_input_desc,
                current_state_output_params_description=current_state_output_desc,
                goal_state_curl=goal_state_curl,
                goal_state_input_params_description=goal_state_input_desc,
                goal_state_output_params_description=goal_state_output_desc,
                error_calculation_curl=error_calculation_curl,
                error_calculation_input_params_description=error_calculation_input_desc,
                error_calculation_output_params_description=error_calculation_output_desc,
                measurements_curl=measurements_curl,
                measurements_input_params_description=measurements_input_desc,
                measurements_output_params_description=measurements_output_desc,
                action_set_curl=action_set_curl,
                action_set_input_params_description=action_set_input_desc,
                action_set_output_params_description=action_set_output_desc,
                analytic_calculation_curl=analytic_calculation_curl,
                analytic_calculation_input_params_description=analytic_calculation_input_desc,
                analytic_calculation_output_params_description=analytic_calculation_output_desc,
                actuation_curl=actuation_curl,
                actuation_input_params_description=actuation_input_desc,
                actuation_output_params_description=actuation_output_desc,
                created_by_user=request.user,
                publishing_history_lookback_memory_size=publishing_history_lookback_memory_size,
                state_action_state_lookback_memory_size=state_action_state_lookback_memory_size,
                topic_messages_history_lookback_memory_size=topic_messages_history_lookback_memory_size
            )

            # Save relations (ManyToMany fields)

            node.subscribed_topics.set(
                subscribed_topics
            )

            node.expert_networks.set(
                expert_networks
            )

        except Exception as e:
            logger.error(f'Error creating node: {e}')
            messages.error(request, f'Error creating node: {e}')

            return redirect(
                'hadron_prime:detail_hadron_system',
                pk=system_id
            )

        logger.info(f'Node created: {node}')
        messages.success(request, 'Node created successfully.')

        return redirect(
            'hadron_prime:detail_hadron_system',
            pk=system_id
        )
