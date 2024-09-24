from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.leanmod.models import ExpertNetworkAssistantReference, LeanAssistant, ExpertNetwork
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CreateLeanAssistantView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )
        context['llm_models'] = LLMCore.objects.filter(
            organization__users__in=[self.request.user]
        )
        context['expert_networks'] = ExpertNetwork.objects.filter(
            organization__in=context['organizations']
        )
        return context

    def post(self, request, *args, **kwargs):
        # Fetch form data
        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        name = request.POST.get('name')
        instructions = request.POST.get('instructions')
        expert_network_ids = request.POST.getlist('expert_networks')
        lean_assistant_image = request.FILES.get('lean_assistant_image')

        # Validate required fields
        if not organization_id or not llm_model_id or not name or not instructions:
            messages.error(request, "Please fill in all required fields.")
            return redirect('leanmod:create')

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/CREATE
        ##############################
        user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_ASSISTANTS not in user_permissions:
            messages.error(self.request, "You do not have permission to add new assistants.")
            return redirect('leanmod:list')
        ##############################

        try:
            # Create new Lean Assistant
            organization = Organization.objects.get(id=organization_id)
            llm_model = LLMCore.objects.get(id=llm_model_id)
            lean_assistant = LeanAssistant.objects.create(
                organization=organization,
                llm_model=llm_model,
                name=name,
                instructions=instructions,
                lean_assistant_image=lean_assistant_image,
                created_by_user=request.user,
                last_updated_by_user=request.user,
            )

            # Add expert networks if selected
            if expert_network_ids:
                for expert_network_id in expert_network_ids:
                    expert_network = ExpertNetwork.objects.get(id=expert_network_id)
                    lean_assistant.expert_networks.add(expert_network)

            lean_assistant.save()
            messages.success(request, "Lean Assistant created successfully.")
            return redirect('leanmod:list')

        except Exception as e:
            messages.error(request, f"Error creating Lean Assistant: {e}")
            return redirect('leanmod:create')


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
        context['selected_expert_networks'] = context['lean_assistant'].expert_networks.all().values_list('id', flat=True)

        return context

    def post(self, request, *args, **kwargs):
        assistant_id = kwargs.get('pk')
        lean_assistant = LeanAssistant.objects.get(id=assistant_id)

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/UPDATE
        ##############################
        user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_ASSISTANTS not in user_permissions:
            messages.error(self.request, "You do not have permission to update/modify assistants.")
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


class DeleteLeanAssistantView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant_id = kwargs.get('pk')
        context['lean_assistant'] = LeanAssistant.objects.get(id=assistant_id)
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/DELETE
        ##############################
        user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_ASSISTANTS not in user_permissions:
            messages.error(self.request, "You do not have permission to delete assistants.")
            return redirect('leanmod:list')
        ##############################

        try:
            lean_assistant = LeanAssistant.objects.get(id=assistant_id)
            lean_assistant.delete()
            messages.success(request, f"Lean Assistant '{lean_assistant.name}' was deleted successfully.")
        except LeanAssistant.DoesNotExist:
            messages.error(request, "The Lean Assistant does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the Lean Assistant: {e}")
        return redirect('leanmod:list')


class ListLeanAssistantsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        org_lean_assistants = {}
        organizations = Organization.objects.prefetch_related('lean_assistants').filter(
            users__in=[self.request.user]
        ).all()

        # Group lean assistants by organization
        for organization in organizations:
            org_lean_assistants[organization] = organization.lean_assistants.all()

        context['org_lean_assistants'] = org_lean_assistants
        return context


####################################################################################################


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
        # PERMISSION CHECK FOR - ASSISTANT/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_ASSISTANTS not in user_permissions:
            messages.error(self.request, "You do not have permission to add / create assistants.")
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
            {'id': ref['assistant_id'], 'name': ref['assistant__name'], 'context_instructions': ref['context_instructions']}
            for ref in assistant_references
        ]
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        expert_network_id = kwargs.get('pk')
        expert_network = ExpertNetwork.objects.get(id=expert_network_id)

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_ASSISTANTS not in user_permissions:
            messages.error(self.request, "You do not have permission to update / modify assistants.")
            return redirect('leanmod:list_expert_networks')
        ##############################

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


class DeleteExpertNetworkView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        expert_network_id = kwargs.get('pk')
        expert_network = get_object_or_404(ExpertNetwork, id=expert_network_id)
        context['expert_network'] = expert_network
        return context

    def post(self, request, *args, **kwargs):
        expert_network_id = kwargs.get('pk')
        expert_network = get_object_or_404(ExpertNetwork, id=expert_network_id)
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_ASSISTANTS not in user_permissions:
            messages.error(self.request, "You do not have permission to delete assistants.")
            return redirect('leanmod:list_expert_networks')
        ##############################

        # Perform the deletion
        expert_network.delete()

        messages.success(request, f'The expert network "{expert_network.name}" has been deleted successfully.')
        return redirect('leanmod:list_expert_networks')


class ListExpertNetworksView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Fetch all expert networks and their related assistants
        expert_networks = ExpertNetwork.objects.prefetch_related('assistant_references__assistant', 'organization').filter(
            organization__users__in=[self.request.user]
        ).all()

        context['expert_networks'] = expert_networks
        return context
