#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_process_list_views.py
#  Last Modified: 2024-10-22 18:38:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:38:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.binexus.models import BinexusProcess
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class BinexusView_ProcessList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_BINEXUS_PROCESSES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_BINEXUS_PROCESSES
        ):
            messages.error(self.request, "You do not have permission to list Binexus Processes.")
            return context
        ##############################

        try:
            user_orgs = Organization.objects.filter(
                users__in=[self.request.user]
            )

            processes_by_org = {
                org: BinexusProcess.objects.filter(
                    organization=org
                )
                for org in user_orgs
            }

            context['processes_by_org'] = processes_by_org

        except Exception as e:
            messages.error(self.request, "Error listing the Binexus Processes.")
            return context

        return context
