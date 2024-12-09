#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_voidforger_connections_views.py
#  Last Modified: 2024-11-15 15:37:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 15:37:18
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
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from apps.voidforger.models import VoidForger


class VoidForgerView_RefreshVoidForgerConnections(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REFRESH_VOIDFORGER_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.REFRESH_VOIDFORGER_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to refresh VoidForger connections.")
            return redirect('voidforger:configuration')
        ##############################

        try:
            voidforger_id = kwargs.get('voidforger_id')
            voidforger = VoidForger.objects.get(id=voidforger_id)

            user_orgs = Organization.objects.filter(
                users__in=[self.request.user]
            )

            voidforger.organizations.set(user_orgs)

        except Exception as e:
            messages.error(self.request, "VoidForger not found.")
            return redirect('voidforger:configuration')

        messages.success(self.request, "VoidForger connections refreshed with all organizations of user.")
        return redirect('voidforger:configuration')
