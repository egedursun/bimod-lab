#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_assistant_connection_views.py
#  Last Modified: 2024-11-13 03:48:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 03:48:20
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.hadron_prime.models import (
    HadronNodeAssistantConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)


class HadronPrimeView_AssistantConnectionDelete(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get("pk")

        ##############################
        # PERMISSION CHECK FOR - DISCONNECT_ASSISTANTS_FROM_HADRON_NODE
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DISCONNECT_ASSISTANTS_FROM_HADRON_NODE
        ):
            messages.error(self.request,
                           "You do not have permission to disconnect an assistant from a Hadron Prime Node.")
            return redirect("hadron_prime:connect_assistant")
        ##############################

        try:
            connection = HadronNodeAssistantConnection.objects.get(
                id=connection_id
            )

            connection.delete()

        except Exception as e:
            messages.error(request, "An error occurred while deleting the connection: " + str(e))

            return redirect("hadron_prime:connect_assistant")

        messages.success(request, "Connection deleted successfully.")

        return redirect("hadron_prime:connect_assistant")
