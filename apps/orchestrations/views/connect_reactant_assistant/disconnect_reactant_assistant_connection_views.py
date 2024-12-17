#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: disconnect_reactant_assistant_connection_views.py
#  Last Modified: 2024-11-13 04:37:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 04:37:46
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

from apps.orchestrations.models import (
    OrchestrationReactantAssistantConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)


class OrchestrationView_AssistantConnectionDelete(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get("pk")

        ##############################
        # PERMISSION CHECK FOR - DISCONNECT_REACTANT_ASSISTANTS_FROM_ORCHESTRATION
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DISCONNECT_REACTANT_ASSISTANTS_FROM_ORCHESTRATION
        ):
            messages.error(
                self.request,
                "You do not have permission to disconnect reactant assistants from an orchestration."
            )

            return redirect("orchestrations:connect_assistant")
        ##############################

        try:
            connection = OrchestrationReactantAssistantConnection.objects.get(
                id=connection_id
            )

            connection.delete()

        except Exception as e:
            messages.error(request, "An error occurred while deleting the connection: " + str(e))

            return redirect("orchestrations:connect_assistant")

        messages.success(request, "Connection deleted successfully.")

        return redirect("orchestrations:connect_assistant")
