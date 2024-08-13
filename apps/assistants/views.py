"""
This module contains views for managing assistants within the Bimod.io platform.

The views include creating, listing, updating, and deleting assistants. Access to these views is restricted to authenticated users, with additional permission checks for certain actions.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant, ASSISTANT_RESPONSE_LANGUAGES, ContextOverflowStrategyNames, \
    CONTEXT_OVERFLOW_STRATEGY, VECTORIZERS, VectorizerNames
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CreateAssistantView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of a new assistant within the Bimod.io platform.

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
        context['vectorizers'] = VECTORIZERS
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_ASSISTANTS not in user_permissions:
            messages.error(request, "You do not have permission to create assistants.")
            return redirect('assistants:list')
        ##############################

        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
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
        assistant_image = request.FILES.get('assistant_image')

        if not (organization_id and llm_model_id and name and description and instructions and audience and tone):
            messages.error(request, "All fields are required.")
            return redirect('assistants:create')

        organization = Organization.objects.get(id=organization_id)
        llm_model = LLMCore.objects.get(id=llm_model_id)

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
            glossary=glossary
        )
        print("[CreateAssistantView.post] Assistant created successfully!")

        # retrieve the assistants of the organization and add the new assistant
        organization.organization_assistants.add(assistant)
        organization.save()
        print("[CreateAssistantView.post] Assistant added to the organization successfully!")

        messages.success(request, "Assistant created successfully!")
        return redirect('assistants:list')


class ListAssistantView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of assistants associated with the user's organizations.

    This view retrieves all assistants that belong to the organizations the user is a part of and displays them in a list. Currently, all authenticated users are allowed to view the list of assistants.

    Methods:
        get_context_data(self, **kwargs): Retrieves the assistants for the user's organizations and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/CREATE
        ##############################
        # for now, we will allow all users to view the list of assistants...
        ##############################

        organizations = Organization.objects.filter(users__in=[user])
        org_assistants = {org: org.assistants.all() for org in organizations}
        context['org_assistants'] = org_assistants
        return context


class UpdateAssistantView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing assistant's details.

    This view allows users with the appropriate permissions to modify an assistant's attributes, including its name, description, instructions, and more. It also handles the logic for updating the assistant's glossary, context overflow strategy, and other configurations.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current assistant's details and adds them to the context, along with other relevant data.
        post(self, request, *args, **kwargs): Handles form submission for updating the assistant, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant_id = self.kwargs.get('pk')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['assistant'] = assistant
        context['response_languages'] = ASSISTANT_RESPONSE_LANGUAGES
        context['context_overflow_strategies'] = CONTEXT_OVERFLOW_STRATEGY
        context['vectorizers'] = VECTORIZERS
        context["assistant_current_strategy"] = ContextOverflowStrategyNames.as_dict()[assistant.context_overflow_strategy]
        context["assistant_current_vectorizer"] = VectorizerNames.as_dict()[assistant.vectorizer_name] if assistant.vectorizer_name else None
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_ASSISTANTS not in user_permissions:
            messages.error(request, "You do not have permission to update / modify assistants.")
            return redirect('assistants:list')
        ##############################

        assistant_id = self.kwargs.get('pk')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        assistant.name = request.POST.get('name')
        assistant.description = request.POST.get('description')
        assistant.instructions = request.POST.get('instructions')
        assistant.audience = request.POST.get('audience')
        assistant.max_retry_count = request.POST.get('max_retry_count')
        assistant.tool_max_attempts_per_instance = request.POST.get('tool_max_attempts_per_instance')
        assistant.tool_max_chains = request.POST.get('tool_max_chains')

        terms = request.POST.getlist('terms[]')
        definitions = request.POST.getlist('definitions[]')
        updated_glossary = {}
        for term, definition in zip(terms, definitions):
            updated_glossary[term] = definition
        assistant.glossary = updated_glossary

        assistant.context_overflow_strategy = request.POST.get('context_overflow_strategy')
        assistant.max_context_messages = request.POST.get('max_context_messages')
        vectorizer_name = None
        vectorizer_api_key = None
        if assistant.context_overflow_strategy == ContextOverflowStrategyNames.FORGET:
            pass
        elif assistant.context_overflow_strategy == ContextOverflowStrategyNames.STOP:
            pass
        elif assistant.context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE:
            vectorizer_name = request.POST.get('vectorizer_name')
            vectorizer_api_key = request.POST.get('vectorizer_api_key')

        assistant.vectorizer_name = vectorizer_name
        assistant.vectorizer_api_key = vectorizer_api_key

        assistant.tone = request.POST.get('tone')
        assistant.llm_model_id = request.POST.get('llm_model')
        assistant.response_template = request.POST.get('response_template')
        assistant.response_language = request.POST.get('response_language')
        assistant.time_awareness = request.POST.get('time_awareness') == 'on'
        assistant.place_awareness = request.POST.get('place_awareness') == 'on'
        assistant.image_generation_capability = request.POST.get('image_generation_capability') == 'on'
        assistant.last_updated_by_user = request.user
        if 'assistant_image' in request.FILES:
            assistant.assistant_image = request.FILES['assistant_image']
        assistant.save()

        return redirect('assistants:update', pk=assistant.id)


class DeleteAssistantView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of an assistant.

    This view allows users with the appropriate permissions to delete an assistant. It checks if the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Adds the assistant to be deleted to the context for confirmation.
        post(self, request, *args, **kwargs): Deletes the assistant if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the assistants that belong to the user's organizations.
    """

    model = Assistant

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant = self.get_object()
        context['assistant'] = assistant
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_ASSISTANTS not in user_permissions:
            messages.error(request, "You do not have permission to delete assistants.")
            return redirect('assistants:list')
        ##############################

        assistant = self.get_object()
        assistant.delete()
        return redirect('assistants:list')

    def get_queryset(self):
        context_user = self.request.user
        return Assistant.objects.filter(organization__users__in=[context_user])
