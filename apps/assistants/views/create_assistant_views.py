#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_assistant_views.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import AGENT_SPEECH_LANGUAGES, CONTEXT_MANAGEMENT_STRATEGY, Assistant
from apps.assistants.utils import ContextManagementStrategyNames
from apps.data_security.models import NERIntegration
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from apps.user_permissions.utils import PermissionNames
from apps.assistants.utils import MULTI_STEP_REASONING_CAPABILITY_CHOICE
from config.settings import MAX_PROJECTS_PER_ASSISTANT
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class AssistantView_Create(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(
            users__in=[
                self.request.user
            ]
        )
        context['llm_models'] = LLMCore.objects.filter(
            organization__in=context['organizations']
        )
        context['response_languages'] = AGENT_SPEECH_LANGUAGES
        context['context_overflow_strategies'] = CONTEXT_MANAGEMENT_STRATEGY
        context['reasoning_capability_choices'] = MULTI_STEP_REASONING_CAPABILITY_CHOICE
        context["ner_integrations"] = NERIntegration.objects.filter(
            organization__in=context['organizations']
        )
        context["projects"] = ProjectItem.objects.filter(
            organization__in=context['organizations']
        )
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_ASSISTANTS
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.ADD_ASSISTANTS
        ):
            messages.error(request, "You do not have permission to create agents.")
            return redirect('assistants:list')
        ##############################

        try:
            org_id = request.POST.get('organization')
            llm_id = request.POST.get('llm_model')
            ner_id = None

            if (
                "ner_integration" in request.POST and
                request.POST.get('ner_integration')
                and request.POST.get('ner_integration') != "None"
                and request.POST.get('ner_integration') != ""
            ):
                ner_id = request.POST.get('ner_integration')
                logger.info(f"NER Integration is defined for this agent. NER ID: {ner_id}")

        except Exception as e:
            logger.error(f"Error while getting the organization and LLM model information: {e}")
            messages.error(request, "Organization and LLM model information is required.")
            return redirect('assistants:create')

        try:
            agent_name = request.POST.get('name')
            agent_description = request.POST.get('description')
            system_instructions = request.POST.get('instructions')
            templated_response = request.POST.get('response_template')
            target_audience = request.POST.get('audience')

            tool_call_max_step_back_retries = request.POST.get('max_retry_count')
            tool_call_chain_same_tool_max = request.POST.get('tool_max_attempts_per_instance')
            tool_call_chain_maximum_attempts = request.POST.get('tool_max_chains')

            terms = request.POST.getlist('terms[]')
            definitions = request.POST.getlist('definitions[]')
            technical_dict = {
                term: definition for term, definition in zip(terms, definitions)
            }

            intra_memory_strategy = request.POST.get('context_overflow_strategy')
            max_msgs_context = request.POST.get('max_context_messages')
            logger.info(f"Agent information is received.")

            if intra_memory_strategy == ContextManagementStrategyNames.FORGET:
                pass

            elif intra_memory_strategy == ContextManagementStrategyNames.STOP:
                pass

            elif intra_memory_strategy == ContextManagementStrategyNames.VECTORIZE:
                pass

            tone = request.POST.get('tone')
            communication_lang = request.POST.get('response_language')
            spatial_capab_time = request.POST.get('time_awareness') == 'on'
            spatial_capab_place = request.POST.get('place_awareness') == 'on'
            visualization_capab = request.POST.get('image_generation_capability') == 'on'
            reasoning_capab = request.POST.get('multi_step_reasoning_capability_choice')
            agent_img = request.FILES.get('assistant_image')

            if not (
                org_id and
                llm_id and
                agent_name and
                agent_description and
                system_instructions and
                target_audience and
                tone
            ):
                messages.error(request, "All fields are required.")
                return redirect('assistants:create')

        except Exception as e:
            logger.error(f"Error while getting the agent information: {e}")
            messages.error(request, "Agent information is required.")
            return redirect('assistants:create')

        try:
            org = Organization.objects.get(id=org_id)
            llm_core = LLMCore.objects.get(id=llm_id)
            ner_integration = None
            if ner_id:
                ner_integration = NERIntegration.objects.get(id=ner_id)

            agent = Assistant.objects.create(
                organization=org,
                llm_model=llm_core,
                name=agent_name,
                description=agent_description,
                instructions=system_instructions,
                audience=target_audience,
                max_retry_count=tool_call_max_step_back_retries,
                tool_max_attempts_per_instance=tool_call_chain_same_tool_max,
                tool_max_chains=tool_call_chain_maximum_attempts,
                tone=tone,
                assistant_image=agent_img,
                context_overflow_strategy=intra_memory_strategy,
                max_context_messages=max_msgs_context,
                created_by_user=context_user,
                last_updated_by_user=context_user,
                response_template=templated_response,
                response_language=communication_lang,
                time_awareness=spatial_capab_time,
                place_awareness=spatial_capab_place,
                image_generation_capability=visualization_capab,
                multi_step_reasoning_capability_choice=reasoning_capab,
                glossary=technical_dict,
                ner_integration=ner_integration
            )

            org.assistants.add(agent)
            org.save()

            project_items = request.POST.getlist('project_items[]', [])
            if project_items and len(project_items) > MAX_PROJECTS_PER_ASSISTANT:
                messages.error(request,
                               f"Maximum related project count is {MAX_PROJECTS_PER_ASSISTANT} per assistant.")
                project_items = project_items[:MAX_PROJECTS_PER_ASSISTANT]

            agent.project_items.set(project_items)
            agent.save()

        except Exception as e:
            logger.error(f"Error while creating the agent: {e}")
            messages.error(request, "Error while creating the agent.")
            return redirect('assistant:create')

        messages.success(request, "Agent created successfully!")
        logger.info(f"Agent is created successfully. Agent ID: {agent.id}")
        return redirect('assistants:list')
