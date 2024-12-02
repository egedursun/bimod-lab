#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_functions.models import CustomFunction, CustomFunctionReference
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_FUNCTIONS_PER_ASSISTANT
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class CustomFunctionView_Connections(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        conn_orgs = Organization.objects.filter(users__in=[user])
        users_of_conn_orgs = [user for org in conn_orgs for user in org.users.all()]
        functions = CustomFunction.objects.filter(created_by_user__in=users_of_conn_orgs)
        ext_function_refs = CustomFunctionReference.objects.filter(assistant__organization__in=conn_orgs).exclude(
            custom_function__created_by_user__in=users_of_conn_orgs)
        agents = Assistant.objects.filter(organization__in=conn_orgs).select_related('organization')
        agent_function_map = {
            assistant.id: CustomFunctionReference.objects.filter(
                assistant=assistant, custom_function__created_by_user__in=users_of_conn_orgs) for assistant in agents}

        ext_function_refs_map = {
            assistant.id: set(reference for reference in ext_function_refs if reference.assistant.id == assistant.id)
            for assistant in agents}

        context.update({
            'connected_organizations': conn_orgs, 'functions': functions, 'assistants': agents,
            'assistant_function_map': agent_function_map, 'external_function_references_map': ext_function_refs_map})
        logger.info(f"User: {self.request.user.id} is connecting functions.")
        return context

    def post(self, request, *args, **kwargs):
        agent_id = request.POST.get('assistant_id')
        function_id = request.POST.get('function_id')
        action = request.POST.get('action')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_FUNCTIONS):
            messages.error(self.request, "You do not have permission to update custom functions.")
            return redirect('mm_functions:list')
        ##############################

        if not agent_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            logger.error(f"Invalid input. Please try again.")
            return redirect('mm_functions:connect')

        try:
            agent = Assistant.objects.get(id=agent_id)

            if action == 'add' and function_id:

                # check the number of function connections assistant has
                n_mm_function_refs = agent.customfunctionreference_set.count()
                if n_mm_function_refs > MAX_FUNCTIONS_PER_ASSISTANT:
                    messages.error(request,
                                   f'Assistant has reached the maximum number of connected functions ({MAX_FUNCTIONS_PER_ASSISTANT}).')
                    return redirect('mm_functions:connect')

                custom_function = CustomFunction.objects.get(id=function_id)

                CustomFunctionReference.objects.create(
                    assistant=agent,
                    custom_function=custom_function,
                    created_by_user=request.user
                )

                logger.info(f"Function '{custom_function.name}' assigned to assistant '{agent.name}'.")
                messages.success(request,
                                 f"Function '{custom_function.name}' assigned to assistant '{agent.name}'.")
            elif action == 'remove':
                ref_id = request.POST.get('reference_id')
                if ref_id:
                    reff = CustomFunctionReference.objects.get(id=ref_id)
                    reff.delete()
                    logger.info(f"Function reference removed from assistant '{agent.name}'.")
                    messages.success(request, f"Function reference removed from assistant '{agent.name}'.")
        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
            logger.error(f"Assistant not found.")
        except CustomFunction.DoesNotExist:
            messages.error(request, "Custom Function not found.")
            logger.error(f"Custom Function not found.")
        except CustomFunctionReference.DoesNotExist:
            messages.error(request, "Custom Function Reference not found.")
            logger.error(f"Custom Function Reference not found.")
        return redirect('mm_functions:connect')
