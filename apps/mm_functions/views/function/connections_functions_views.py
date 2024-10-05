#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: connections_functions_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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
from apps.mm_functions.models import CustomFunction, CustomFunctionReference
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ManageCustomFunctionAssistantConnectionsView(LoginRequiredMixin, TemplateView):
    """
    Manages the connections between custom functions and assistants.

    This view allows users to assign or remove custom functions from their assistants, ensuring the correct integrations are in place.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the available assistants, custom functions, and their connections.
        post(self, request, *args, **kwargs): Processes the request to either add or remove a custom function connection from an assistant.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[user])

        # Retrieve all users of the connected organizations
        users_of_connected_organizations = [user for org in connected_organizations for user in org.users.all()]

        # Fetch internal functions created by users of connected organizations
        functions = CustomFunction.objects.filter(created_by_user__in=users_of_connected_organizations)

        # Fetch external functions
        external_function_references = CustomFunctionReference.objects.filter(
            assistant__organization__in=connected_organizations
        ).exclude(custom_function__created_by_user__in=users_of_connected_organizations)

        # Fetch all assistants in connected organizations
        assistants = Assistant.objects.filter(organization__in=connected_organizations).select_related('organization')

        # Create a dictionary mapping assistants to their custom function references
        assistant_function_map = {
            assistant.id: CustomFunctionReference.objects.filter(
                assistant=assistant,
                custom_function__created_by_user__in=users_of_connected_organizations
            )
            for assistant in assistants
        }

        external_function_references_map = {
            assistant.id: set(
                reference for reference in external_function_references if reference.assistant.id == assistant.id)
            for assistant in assistants
        }

        context.update({
            'connected_organizations': connected_organizations,
            'functions': functions,
            'assistants': assistants,
            'assistant_function_map': assistant_function_map,
            'external_function_references_map': external_function_references_map
        })
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant_id')
        function_id = request.POST.get('function_id')
        action = request.POST.get('action')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_FUNCTIONS):
            messages.error(self.request, "You do not have permission to update custom functions.")
            return redirect('mm_functions:list')
        ##############################

        if not assistant_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            return redirect('mm_functions:connect')

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            if action == 'add' and function_id:
                custom_function = CustomFunction.objects.get(id=function_id)
                CustomFunctionReference.objects.create(
                    assistant=assistant,
                    custom_function=custom_function,
                    created_by_user=request.user
                )
                print(
                    f"[ManageCustomFunctionAssistantConnectionsView.post] Function '{custom_function.name}' assigned to assistant '{assistant.name}'.")
                messages.success(request,
                                 f"Function '{custom_function.name}' assigned to assistant '{assistant.name}'.")
            elif action == 'remove':
                reference_id = request.POST.get('reference_id')
                if reference_id:
                    reference = CustomFunctionReference.objects.get(id=reference_id)
                    reference.delete()
                    messages.success(request, f"Function reference removed from assistant '{assistant.name}'.")
        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
        except CustomFunction.DoesNotExist:
            messages.error(request, "Custom Function not found.")
        except CustomFunctionReference.DoesNotExist:
            messages.error(request, "Custom Function Reference not found.")

        return redirect('mm_functions:connect')
