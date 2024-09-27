from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.finetuning.models import FineTunedModelConnection
from apps.llm_core.forms import LLMCoreForm
from apps.llm_core.models import LLMCore
from apps.llm_core.utils import LLM_CORE_PROVIDERS, OPENAI_GPT_MODEL_NAMES
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
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
        # Add the custom fine-tuning models to the model name choices
        ##########################################
        fine_tuned_models = FineTunedModelConnection.objects.filter(
            organization__in=context['organizations']
        ).all()
        for model in fine_tuned_models:
            if model.model_name not in [m[0] for m in context['model_name_choices']]:
                context['model_name_choices'].append((model.model_name, model.nickname))
        for model in context['model_name_choices']:
            if model[0] not in [m[0] for m in OPENAI_GPT_MODEL_NAMES] and model[0] not in [m[0] for m in
                                                                                           fine_tuned_models]:
                context['model_name_choices'].remove(model)

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_LLM_CORES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_LLM_CORES):
            messages.error(self.request, "You do not have permission to add LLM Cores.")
            return redirect('llm_core:list')
        ##############################

        form = LLMCoreForm(request.POST, request.FILES)
        user = request.user

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
