#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import ASSISTANT_RESPONSE_LANGUAGES, CONTEXT_OVERFLOW_STRATEGY, VECTORIZERS, Assistant
from apps.assistants.utils import ContextOverflowStrategyNames
from apps.data_security.models import NERIntegration
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from apps.assistants.utils import MULTI_STEP_REASONING_CAPABILITY_CHOICE
from web_project import TemplateLayout


class CreateAssistantView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of a new assistant within the Br6.in platform.

    This view displays a form for creating an assistant, and upon submission, it validates the input, checks user permissions, and saves the new assistant to the database. If the user lacks the necessary permissions, an error message is displayed.

    Attributes:
        template_name (str): The template used to render the assistant creation form.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, such as available organizations, LLM models, and other necessary data for creating an assistant.
        post(self, request, *args, **kwargs): Handles form submission and assistant creation, including permission checks and validation.
    """

    template_name = "assistants/create_assistant.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['response_languages'] = ASSISTANT_RESPONSE_LANGUAGES
        context['context_overflow_strategies'] = CONTEXT_OVERFLOW_STRATEGY
        context['reasoning_capability_choices'] = MULTI_STEP_REASONING_CAPABILITY_CHOICE
        context['vectorizers'] = VECTORIZERS
        context["ner_integrations"] = NERIntegration.objects.filter(
            organization__in=context['organizations']
        )
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=context_user, operation=PermissionNames.ADD_ASSISTANTS):
            messages.error(request, "You do not have permission to create assistants.")
            return redirect('assistants:list')
        ##############################

        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')

        # Retrieve the NER integration ID, or leave NULL if not provided
        ner_integration_id = None
        if ("ner_integration" in request.POST and request.POST.get('ner_integration')
            and request.POST.get('ner_integration') != "None"
            and request.POST.get('ner_integration') != ""):
            ner_integration_id = request.POST.get('ner_integration')

        name = request.POST.get('name')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        response_template = request.POST.get('response_template')
        audience = request.POST.get('audience')
        max_retry_count = request.POST.get('max_retry_count')
        tool_max_attempts_per_instance = request.POST.get('tool_max_attempts_per_instance')
        tool_max_chains = request.POST.get('tool_max_chains')

        terms = request.POST.getlist('terms[]')
        definitions = request.POST.getlist('definitions[]')
        glossary = {term: definition for term, definition in zip(terms, definitions)}

        context_overflow_strategy = request.POST.get('context_overflow_strategy')
        max_context_messages = request.POST.get('max_context_messages')
        vectorizer_name = None
        vectorizer_api_key = None
        if context_overflow_strategy == ContextOverflowStrategyNames.FORGET:
            pass
        elif context_overflow_strategy == ContextOverflowStrategyNames.STOP:
            pass
        elif context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE:
            vectorizer_name = request.POST.get('vectorizer_name')
            vectorizer_api_key = request.POST.get('vectorizer_api_key')

        tone = request.POST.get('tone')
        response_language = request.POST.get('response_language')
        time_awareness = request.POST.get('time_awareness') == 'on'
        place_awareness = request.POST.get('place_awareness') == 'on'
        image_generation_capability = request.POST.get('image_generation_capability') == 'on'
        reasoning_capability_choice = request.POST.get('multi_step_reasoning_capability_choice')
        assistant_image = request.FILES.get('assistant_image')

        if not (organization_id and llm_model_id and name and description and instructions and audience and tone):
            messages.error(request, "All fields are required.")
            return redirect('assistants:create')

        organization = Organization.objects.get(id=organization_id)
        llm_model = LLMCore.objects.get(id=llm_model_id)

        # Retrieve and assign NER integration, or leave NULL if not provided
        ner_integration = None
        if ner_integration_id:
            ner_integration = NERIntegration.objects.get(id=ner_integration_id)

        assistant = Assistant.objects.create(
            organization=organization,
            llm_model=llm_model,
            name=name,
            description=description,
            instructions=instructions,
            audience=audience,
            max_retry_count=max_retry_count,
            tool_max_attempts_per_instance=tool_max_attempts_per_instance,
            tool_max_chains=tool_max_chains,
            tone=tone,
            assistant_image=assistant_image,
            context_overflow_strategy=context_overflow_strategy,
            max_context_messages=max_context_messages,
            vectorizer_name=vectorizer_name,
            vectorizer_api_key=vectorizer_api_key,
            created_by_user=context_user,
            last_updated_by_user=context_user,
            response_template=response_template,
            response_language=response_language,
            time_awareness=time_awareness,
            place_awareness=place_awareness,
            image_generation_capability=image_generation_capability,
            multi_step_reasoning_capability_choice=reasoning_capability_choice,
            glossary=glossary,
            ner_integration=ner_integration
        )
        print("[CreateAssistantView.post] Assistant created successfully!")

        # retrieve the assistants of the organization and add the new assistant
        organization.assistants.add(assistant)
        organization.save()
        print("[CreateAssistantView.post] Assistant added to the organization successfully!")

        messages.success(request, "Assistant created successfully!")
        return redirect('assistants:list')
