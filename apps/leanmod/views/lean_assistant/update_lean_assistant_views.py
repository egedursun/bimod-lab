from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import LeanAssistant, ExpertNetwork
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class UpdateLeanAssistantView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant_id = kwargs.get('pk')
        context['lean_assistant'] = LeanAssistant.objects.get(id=assistant_id)

        # Populate the dropdowns with existing data
        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )
        context['llm_models'] = LLMCore.objects.filter(
            organization__users__in=[self.request.user]
        )
        context['expert_networks'] = ExpertNetwork.objects.filter(
            organization__in=context['organizations']
        )
        context['selected_expert_networks'] = context['lean_assistant'].expert_networks.all().values_list('id',
                                                                                                          flat=True)

        return context

    def post(self, request, *args, **kwargs):
        assistant_id = kwargs.get('pk')
        lean_assistant = LeanAssistant.objects.get(id=assistant_id)

        ##############################
        # PERMISSION CHECK FOR - UPDATE_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_LEAN_ASSISTANT):
            messages.error(self.request, "You do not have permission to update LeanMod assistants.")
            return redirect('leanmod:list')
        ##############################

        # Fetch form data
        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        name = request.POST.get('name')
        instructions = request.POST.get('instructions')
        expert_network_ids = request.POST.getlist('expert_networks')
        lean_assistant_image = request.FILES.get('lean_assistant_image', None)

        # Validate required fields
        if not organization_id or not llm_model_id or not name or not instructions:
            messages.error(request, "Please fill in all required fields.")
            return redirect('leanmod:update', pk=assistant_id)

        try:
            # Update Lean Assistant
            lean_assistant.organization = Organization.objects.get(id=organization_id)
            lean_assistant.llm_model = LLMCore.objects.get(id=llm_model_id)
            lean_assistant.name = name
            lean_assistant.instructions = instructions

            if lean_assistant_image:
                lean_assistant.lean_assistant_image = lean_assistant_image

            # Update expert networks
            lean_assistant.expert_networks.clear()
            if expert_network_ids:
                for expert_network_id in expert_network_ids:
                    expert_network = ExpertNetwork.objects.get(id=expert_network_id)
                    lean_assistant.expert_networks.add(expert_network)

            lean_assistant.save()
            messages.success(request, "Lean Assistant updated successfully.")
            return redirect('leanmod:list')

        except Exception as e:
            messages.error(request, f"Error updating Lean Assistant: {e}")
            return redirect('leanmod:update', pk=assistant_id)
