from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_apis.models import CustomAPI, CustomAPIReference
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ManageCustomAPIAssistantConnectionsView(LoginRequiredMixin, TemplateView):
    """
    Manages the connections between custom APIs and assistants.

    This view allows users to assign or remove custom APIs from their assistants, ensuring the correct integrations are in place.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the available assistants, custom APIs, and their connections.
        post(self, request, *args, **kwargs): Processes the request to either add or remove a custom API connection from an assistant.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[user])

        # Retrieve all users of the connected organizations
        users_of_connected_organizations = [user for org in connected_organizations for user in org.users.all()]
        # Fetch internal APIs created by users of connected organizations
        apis = CustomAPI.objects.filter(created_by_user__in=users_of_connected_organizations)
        # Fetch external API references
        external_api_references = CustomAPIReference.objects.filter(
            assistant__organization__in=connected_organizations
        ).exclude(custom_api__created_by_user__in=users_of_connected_organizations)
        # Fetch all assistants in connected organizations
        assistants = Assistant.objects.filter(organization__in=connected_organizations).select_related('organization')
        # Create a dictionary mapping assistants to their custom API references
        assistant_api_map = {
            assistant.id: CustomAPIReference.objects.filter(
                assistant=assistant, custom_api__created_by_user__in=users_of_connected_organizations
            )
            for assistant in assistants
        }

        external_api_references_map = {
            assistant.id: set(
                reference for reference in external_api_references if reference.assistant.id == assistant.id)
            for assistant in assistants
        }

        context.update({
            'connected_organizations': connected_organizations, 'apis': apis, 'assistants': assistants,
            'assistant_api_map': assistant_api_map, 'external_api_references_map': external_api_references_map
        })
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_APIS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_APIS):
            messages.error(self.request, "You do not have permission to update custom APIs.")
            return redirect('mm_apis:list')
        ##############################

        assistant_id = request.POST.get('assistant_id')
        api_id = request.POST.get('api_id')
        action = request.POST.get('action')
        # PERMISSION CHECK FOR - ADD_APIS
        user_permissions = UserPermission.active_permissions.filter(user=request.user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_APIS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add API connections."}
            return self.render_to_response(context)

        if not assistant_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            return redirect('mm_apis:connect')
        try:
            assistant = Assistant.objects.get(id=assistant_id)
            if action == 'add' and api_id:
                custom_api = CustomAPI.objects.get(id=api_id)
                CustomAPIReference.objects.create(
                    assistant=assistant, custom_api=custom_api, created_by_user=request.user
                )
                messages.success(request, f"API '{custom_api.name}' assigned to assistant '{assistant.name}'.")
            elif action == 'remove':
                reference_id = request.POST.get('reference_id')
                if reference_id:
                    reference = CustomAPIReference.objects.get(id=reference_id)
                    reference.delete()
                    messages.success(request, f"API reference removed from assistant '{assistant.name}'.")
                    print(
                        f"[ManageCustomAPIAssistantConnectionsView.post] API reference removed from assistant '{assistant.name}'.")
        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
        except CustomAPI.DoesNotExist:
            messages.error(request, "Custom API not found.")
        except CustomAPIReference.DoesNotExist:
            messages.error(request, "Custom API Reference not found.")
        return redirect('mm_apis:connect')
