"""
This module provides views for managing LLM Core models within the Bimod.io platform.

The views allow authenticated users to create, list, update, and delete LLM Core models, while enforcing necessary permission checks to ensure that users have the appropriate access rights.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.finetuning.models import FineTunedModelConnection
from apps.llm_core.forms import LLMCoreForm
from apps.llm_core.models import LLM_CORE_PROVIDERS, OPENAI_GPT_MODEL_NAMES, LLMCore
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames, UserPermission
from web_project import TemplateLayout


class CreateLLMCoreView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of a new LLM Core model.

    This view allows users with the appropriate permissions to create a new LLM Core model, associate it with an organization, and set various properties such as the provider and model name.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with available organizations, providers, and model names.
        post(self, request, *args, **kwargs): Processes the form submission for creating a new LLM Core model, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        context['user'] = user
        context['organizations'] = user.organizations.all()
        context['provider_choices'] = LLM_CORE_PROVIDERS
        context['model_name_choices'] = OPENAI_GPT_MODEL_NAMES

        ##########################################
        # TODO-2: Add the custom fine-tuning models to the model name choices
        # ...
        ##########################################
        fine_tuned_models = FineTunedModelConnection.objects.filter(
            organization__in=user.organizations.all()
        ).all()
        for model in fine_tuned_models:
            if model.model_name not in [m[0] for m in context['model_name_choices']]:
                context['model_name_choices'].append((model.model_name, model.nickname))

        return context

    def post(self, request, *args, **kwargs):
        form = LLMCoreForm(request.POST, request.FILES)
        user = request.user
        # PERMISSION CHECK FOR - LLM/CREATE
        user_permissions = UserPermission.active_permissions.filter(user=user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_LLM_CORES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add LLM Cores."}
            return self.render_to_response(context)

        form.instance.created_by_user = user
        form.instance.last_updated_by_user = user
        if form.is_valid():
            form.save()
            # add llm model to the organization
            organization = Organization.objects.get(id=request.POST['organization'])
            llm_core = LLMCore.objects.filter(created_by_user=user).latest('created_at')
            organization.llm_cores.add(llm_core)
            organization.save()
            return redirect('llm_core:list')
        else:
            error_messages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messages
            return self.render_to_response(context)


class ListLLMCoreView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all LLM Core models associated with the user's organizations.

    This view retrieves all LLM Core models linked to the organizations that the user belongs to and displays them.

    Methods:
        get_context_data(self, **kwargs): Retrieves the LLM Core models for the user's organizations and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        organizations = user.organizations.all()
        # PERMISSION CHECK FOR - LLM/LIST
        # For now, every user is able to see the LLM cores.

        # retrieve the llm cores for every organization and store in the dictionary
        llm_cores = {}
        for organization in organizations:
            llm_cores[organization] = organization.llm_cores.all()
        context['organizations'] = organizations
        context['org_llm_cores'] = llm_cores
        return context


class UpdateLLMCoreView(TemplateView, LoginRequiredMixin):
    """
    Handles updating an existing LLM Core model.

    This view allows users with the appropriate permissions to modify an existing LLM Core model's attributes, such as the organization it is associated with, provider, and model name.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current LLM Core model details and adds them to the context, along with other relevant data such as available organizations, providers, and model names.
        post(self, request, *args, **kwargs): Processes the form submission for updating the LLM Core model, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        llm_core = LLMCore.objects.get(id=kwargs['pk'])
        context_user = self.request.user
        context['llm_core'] = llm_core
        context['organizations'] = context_user.organizations.all()
        context['provider_choices'] = LLM_CORE_PROVIDERS
        context['model_name_choices'] = OPENAI_GPT_MODEL_NAMES
        return context

    def post(self, request, *args, **kwargs):
        llm_core = LLMCore.objects.get(id=kwargs['pk'])
        prev_organization = llm_core.organization
        form = LLMCoreForm(request.POST, request.FILES, instance=llm_core)
        context_user = request.user
        # PERMISSION CHECK FOR - LLM/UPDATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.UPDATE_LLM_CORES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update or modify LLM Cores."}
            return self.render_to_response(context)

        if form.is_valid():
            prev_organization.llm_cores.remove(llm_core)
            prev_organization.save()
            form.save()
            organization = Organization.objects.get(id=request.POST['organization'])
            organization.llm_cores.add(llm_core)
            organization.save()
            return redirect('llm_core:list')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            error_messages = form.errors
            context['error_messages'] = error_messages
            return self.render_to_response(context)


class DeleteLLMCoreView(DeleteView, LoginRequiredMixin):
    """
    Handles the deletion of an LLM Core model.

    This view allows users with the appropriate permissions to delete an LLM Core model and remove it from the associated organization.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the current user's details.
        post(self, request, *args, **kwargs): Deletes the LLM Core model if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the LLM Core models associated with the user's organizations.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        context['user'] = user
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        # PERMISSION CHECK FOR - LLM/DELETE
        user_permissions = UserPermission.active_permissions.filter(user=user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.DELETE_LLM_CORES not in user_permissions:
            messages.error(request, "You do not have permission to delete LLM Cores.")
            return redirect('llm_core:list')

        llm_core = get_object_or_404(LLMCore, id=kwargs['pk'])
        llm_core.delete()
        return redirect('llm_core:list')

    def get_queryset(self):
        user = self.request.user
        return LLMCore.objects.filter(organizations__in=user.organizations.all())
