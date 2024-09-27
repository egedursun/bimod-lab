from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.leanmod.models import ExpertNetwork, ExpertNetworkAssistantReference
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class CreateExpertNetworkView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['assistants'] = Assistant.objects.filter(organization__users__in=[user])
        context['organizations'] = Organization.objects.filter(users__in=[user])
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_EXPERT_NETWORK
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to add Expert Network.")
            return redirect('leanmod:list_expert_networks')
        ##############################

        # Get data from form
        name = request.POST.get("network_name")
        description = request.POST.get("network_description")
        selected_assistant_ids = request.POST.getlist("assistants")
        organization_id = request.POST.get("organization")

        print("[CreateExpertNetworkView.post] Selected Assistants: ", selected_assistant_ids)
        print("[CreateExpertNetworkView.post] Selected Organization: ", organization_id)

        # Get the organization
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            messages.error(request, "Selected organization does not exist.")
            return redirect('leanmod:create_expert_network')

        # Create the Expert Network
        try:
            expert_network = ExpertNetwork.objects.create(
                name=name,
                meta_description=description,
                organization=organization,  # Add organization to the new expert network
                created_by_user=request.user,
                last_updated_by_user=request.user
            )
        except Exception as e:
            messages.error(request, f"Error creating Expert Network: {e}")
            print("[CreateExpertNetworkView.post] Error creating Expert Network: ", e)
            return redirect('leanmod:create_expert_network')

        # Create the Assistant references with context instructions
        for assistant_id in selected_assistant_ids:
            assistant = Assistant.objects.get(id=assistant_id)
            context_instructions = request.POST.get(f"context_instructions_{assistant_id}")

            try:
                reference = ExpertNetworkAssistantReference.objects.create(
                    network=expert_network,
                    assistant=assistant,
                    context_instructions=context_instructions,
                    created_by_user=request.user,
                    last_updated_by_user=request.user
                )
                expert_network.assistant_references.add(reference)
                expert_network.save()
            except Exception as e:
                messages.error(request, f"Error creating Expert Network Assistant Reference: {e}")
                print("[CreateExpertNetworkView.post] Error creating Expert Network Assistant Reference: ", e)
                return redirect('leanmod:create_expert_network')

        messages.success(request, "Expert Network created successfully with selected assistants.")
        return redirect('leanmod:list_expert_networks')
