#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: trigger_voidforger_run_views.py
#  Last Modified: 2024-11-14 22:34:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 22:34:34
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

from apps.core.tool_calls.utils import (
    VoidForgerModesNames
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.core.voidforger.voidforger_executor import (
    VoidForgerExecutionManager
)

from apps.user_permissions.utils import (
    PermissionNames
)


class VoidForgerView_ManualTriggerVoidForgerRun(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - MANUALLY_TRIGGER_VOIDFORGER
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.MANUALLY_TRIGGER_VOIDFORGER
        ):
            messages.error(self.request, "You do not have permission to manually trigger VoidForger runs.")
            return redirect('voidforger:configuration')
        ##############################

        try:
            voidforger_id = kwargs.get('voidforger_id')

            xc = VoidForgerExecutionManager(
                user=self.request.user,
                voidforger_id=voidforger_id
            )

            error = xc.run_cycle(
                trigger=VoidForgerModesNames.MANUAL
            )

            if error:
                messages.error(self.request, "VoidForger execution has failed: " + str(error))

                return redirect('voidforger:configuration')

        except Exception as e:
            messages.error(self.request, "VoidForger execution has failed: " + str(e))

            return redirect('voidforger:configuration')

        messages.success(self.request, "VoidForger execution has been triggered successfully.")

        return redirect('voidforger:configuration')
