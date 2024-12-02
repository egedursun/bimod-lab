#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_scripts.models import CustomScript, CustomScriptReference
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_SCRIPTS_PER_ASSISTANT
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class CustomScriptView_Connections(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        conn_orgs = Organization.objects.filter(users__in=[user])
        users_of_conn_orgs = [user for org in conn_orgs for user in org.users.all()]
        scripts = CustomScript.objects.filter(created_by_user__in=users_of_conn_orgs)
        ext_script_refs = CustomScriptReference.objects.filter(assistant__organization__in=conn_orgs).exclude(
            custom_script__created_by_user__in=users_of_conn_orgs)
        agents = Assistant.objects.filter(organization__in=conn_orgs).select_related('organization')
        agent_script_map = {
            assistant.id: CustomScriptReference.objects.filter(
                assistant=assistant, custom_script__created_by_user__in=users_of_conn_orgs) for assistant in agents}
        ext_script_refs_map = {
            assistant.id: set(reference for reference in ext_script_refs if reference.assistant.id == assistant.id)
            for assistant in agents}
        context.update({
            'connected_organizations': conn_orgs, 'scripts': scripts, 'assistants': agents,
            'assistant_script_map': agent_script_map, 'external_script_references_map': ext_script_refs_map})
        return context

    def post(self, request, *args, **kwargs):
        agent_id = request.POST.get('assistant_id')
        script_id = request.POST.get('script_id')
        action = request.POST.get('action')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SCRIPTS):
            messages.error(self.request, "You do not have permission to update scripts.")
            return redirect('mm_scripts:list')
        ##############################

        if not agent_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            logger.error(f"Invalid input. Please try again.")
            return redirect('mm_scripts:connect')

        try:

            agent = Assistant.objects.get(id=agent_id)

            if action == 'add' and script_id:

                # check the number of script connections assistant has
                n_mm_script_refs = agent.customscriptreference_set.count()

                if n_mm_script_refs > MAX_SCRIPTS_PER_ASSISTANT:
                    messages.error(request,
                                   f'Assistant has reached the maximum number of connected scripts ({MAX_SCRIPTS_PER_ASSISTANT}).')
                    return redirect('mm_scripts:connect')

                custom_script = CustomScript.objects.get(id=script_id)

                CustomScriptReference.objects.create(
                    assistant=agent,
                    custom_script=custom_script,
                    created_by_user=request.user
                )

                logger.info(f"Script '{custom_script.name}' assigned to assistant '{agent.name}'.")
                messages.success(request, f"Script '{custom_script.name}' assigned to assistant '{agent.name}'.")

            elif action == 'remove':
                ref_id = request.POST.get('reference_id')
                if ref_id:
                    ref = CustomScriptReference.objects.get(id=ref_id)
                    ref.delete()
                    logger.info(f"Script reference removed from assistant '{agent.name}'.")
                    messages.success(request, f"Script reference removed from assistant '{agent.name}'.")

        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
            logger.error(f"Assistant not found.")

        except CustomScript.DoesNotExist:
            logger.error(f"Custom Script not found.")
            messages.error(request, "Custom Script not found.")

        except CustomScriptReference.DoesNotExist:
            logger.error(f"Custom Script Reference not found.")
            messages.error(request, "Custom Script Reference not found.")

        return redirect('mm_scripts:connect')
