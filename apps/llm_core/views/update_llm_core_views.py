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
        # PERMISSION CHECK FOR - UPDATE_LLM_CORES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_LLM_CORES):
            messages.error(self.request, "You do not have permission to update LLM Cores.")
            return redirect('llm_core:list')
        ##############################

        llm_core = LLMCore.objects.get(id=kwargs['pk'])
        prev_organization = llm_core.organization
        form = LLMCoreForm(request.POST, request.FILES, instance=llm_core)

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
