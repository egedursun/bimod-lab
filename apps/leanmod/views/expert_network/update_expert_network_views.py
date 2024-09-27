from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.leanmod.models import ExpertNetwork, ExpertNetworkAssistantReference
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class UpdateExpertNetworkView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        expert_network_id = kwargs.get('pk')
        expert_network = ExpertNetwork.objects.get(id=expert_network_id)
        assistants = Assistant.objects.filter(organization__users__in=[user])

        # Fetch all assistant references for the expert network
        assistant_references = expert_network.assistant_references.all().values(
            'assistant_id', 'assistant__name', 'context_instructions'
        )

        # Prepare data for the frontend
        context['expert_network'] = expert_network
        context['assistants'] = assistants
        context['assistant_references'] = [
            {'id': ref['assistant_id'], 'name': ref['assistant__name'],
             'context_instructions': ref['context_instructions']}
            for ref in assistant_references
        ]
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to update Expert Network.")
            return redirect('leanmod:list_expert_networks')
        ##############################

        user = self.request.user
        expert_network_id = kwargs.get('pk')
        expert_network = ExpertNetwork.objects.get(id=expert_network_id)

        # Update basic fields
        expert_network.name = request.POST.get("network_name")
        expert_network.meta_description = request.POST.get("network_description")
        expert_network.save()

        # Remove existing assistant references
        expert_network.assistant_references.clear()

        # Update the Assistant references
        selected_assistant_ids = request.POST.getlist("assistants")
        for assistant_id in selected_assistant_ids:
            assistant = Assistant.objects.get(id=assistant_id)
            context_instructions = request.POST.get(f"context_instructions_{assistant_id}")

            reference, created = ExpertNetworkAssistantReference.objects.get_or_create(
                network=expert_network,
                assistant=assistant,
                defaults={
                    'context_instructions': context_instructions,
                    'created_by_user': request.user,
                    'last_updated_by_user': request.user,
                }
            )
            if not created:
                reference.context_instructions = context_instructions
                reference.last_updated_by_user = request.user
                reference.save()

            expert_network.assistant_references.add(reference)

        messages.success(request, "Expert Network updated successfully.")
        return redirect('leanmod:update_expert_network', pk=expert_network_id)
