#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: connections_scripts_views.py
#  Last Modified: 2024-10-05 01:39:48
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
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_scripts.models import CustomScript, CustomScriptReference
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ManageCustomScriptAssistantConnectionsView(LoginRequiredMixin, TemplateView):
    """
    Manages the connections between custom scripts and assistants.

    This view allows users to assign or remove custom scripts from their assistants. The view checks user permissions before allowing these actions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with data about available custom scripts and assistants.
        post(self, request, *args, **kwargs): Processes the form submission to add or remove custom script connections for assistants.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[user])
        # Retrieve all users of the connected organizations
        users_of_connected_organizations = [user for org in connected_organizations for user in org.users.all()]
        # Fetch internal scripts created by users of connected organizations
        scripts = CustomScript.objects.filter(created_by_user__in=users_of_connected_organizations)
        # Fetch external script references
        external_script_references = CustomScriptReference.objects.filter(
            assistant__organization__in=connected_organizations
        ).exclude(custom_script__created_by_user__in=users_of_connected_organizations)
        # Fetch all assistants in connected organizations
        assistants = Assistant.objects.filter(organization__in=connected_organizations).select_related('organization')
        # Create a dictionary mapping assistants to their custom script references
        assistant_script_map = {
            assistant.id: CustomScriptReference.objects.filter(
                assistant=assistant, custom_script__created_by_user__in=users_of_connected_organizations
            ) for assistant in assistants
        }
        external_script_references_map = {
            assistant.id: set(
                reference for reference in external_script_references if reference.assistant.id == assistant.id)
            for assistant in assistants
        }
        context.update({
            'connected_organizations': connected_organizations, 'scripts': scripts, 'assistants': assistants,
            'assistant_script_map': assistant_script_map,
            'external_script_references_map': external_script_references_map
        })
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant_id')
        script_id = request.POST.get('script_id')
        action = request.POST.get('action')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SCRIPTS):
            messages.error(self.request, "You do not have permission to update scripts.")
            return redirect('mm_scripts:list')
        ##############################

        if not assistant_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            return redirect('mm_scripts:connect')
        try:
            assistant = Assistant.objects.get(id=assistant_id)
            if action == 'add' and script_id:
                custom_script = CustomScript.objects.get(id=script_id)
                CustomScriptReference.objects.create(
                    assistant=assistant, custom_script=custom_script, created_by_user=request.user
                )
                messages.success(request, f"Script '{custom_script.name}' assigned to assistant '{assistant.name}'.")
            elif action == 'remove':
                reference_id = request.POST.get('reference_id')
                if reference_id:
                    reference = CustomScriptReference.objects.get(id=reference_id)
                    reference.delete()
                    print(f"Script reference removed from assistant '{assistant.name}'.")
                    messages.success(request, f"Script reference removed from assistant '{assistant.name}'.")
        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
        except CustomScript.DoesNotExist:
            messages.error(request, "Custom Script not found.")
        except CustomScriptReference.DoesNotExist:
            messages.error(request, "Custom Script Reference not found.")
        return redirect('mm_scripts:connect')
