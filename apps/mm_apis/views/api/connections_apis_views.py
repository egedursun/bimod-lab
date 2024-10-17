#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connections_apis_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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
from apps.mm_apis.models import CustomAPI, CustomAPIReference
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class CustomAPIView_Connections(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        conn_orgs = Organization.objects.filter(users__in=[user])
        users_of_conn_orgs = [user for org in conn_orgs for user in org.users.all()]
        apis = CustomAPI.objects.filter(created_by_user__in=users_of_conn_orgs)
        ext_api_refs = CustomAPIReference.objects.filter(assistant__organization__in=conn_orgs).exclude(
            custom_api__created_by_user__in=users_of_conn_orgs)
        agents = Assistant.objects.filter(organization__in=conn_orgs).select_related('organization')
        agent_api_map = {
            assistant.id: CustomAPIReference.objects.filter(
                assistant=assistant, custom_api__created_by_user__in=users_of_conn_orgs) for assistant in agents }

        ext_api_refs_map = {
            assistant.id: set(
                ref for ref in ext_api_refs if ref.assistant.id == assistant.id)
            for assistant in agents
        }
        context.update({
            'connected_organizations': conn_orgs, 'apis': apis, 'assistants': agents,
            'assistant_api_map': agent_api_map, 'external_api_references_map': ext_api_refs_map
        })
        logger.info(f"User: {self.request.user.id} is connecting APIs.")
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_APIS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_APIS):
            messages.error(self.request, "You do not have permission to update custom APIs.")
            return redirect('mm_apis:list')
        ##############################

        agent_id = request.POST.get('assistant_id')
        api_id = request.POST.get('api_id')
        action = request.POST.get('action')

        if not agent_id or not action:
            logger.error(f"Invalid input. Please try again.")
            messages.error(request, "Invalid input. Please try again.")
            return redirect('mm_apis:connect')
        try:
            agent = Assistant.objects.get(id=agent_id)
            if action == 'add' and api_id:
                custom_api = CustomAPI.objects.get(id=api_id)
                CustomAPIReference.objects.create(assistant=agent, custom_api=custom_api, created_by_user=request.user)
                logger.info(f"API '{custom_api.name}' assigned to assistant '{agent.name}'.")
                messages.success(request, f"API '{custom_api.name}' assigned to assistant '{agent.name}'.")
            elif action == 'remove':
                ref_id = request.POST.get('reference_id')
                if ref_id:
                    reff = CustomAPIReference.objects.get(id=ref_id)
                    reff.delete()
                    logger.info(f"API reference removed from assistant '{agent.name}'.")
                    messages.success(request, f"API reference removed from assistant '{agent.name}'.")
        except Assistant.DoesNotExist:
            logger.error(f"Assistant not found.")
            messages.error(request, "Assistant not found.")
        except CustomAPI.DoesNotExist:
            logger.error(f"Custom API not found.")
            messages.error(request, "Custom API not found.")
        except CustomAPIReference.DoesNotExist:
            logger.error(f"Custom API Reference not found.")
            messages.error(request, "Custom API Reference not found.")
        return redirect('mm_apis:connect')
