#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: toggle_auto_run_voidforger_views.py
#  Last Modified: 2024-11-14 22:31:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:54:11
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

from apps.user_permissions.utils import (
    PermissionNames
)

from apps.voidforger.models import (
    VoidForger,
    VoidForgerToggleAutoExecutionLog
)

from apps.voidforger.utils import (
    VoidForgerRuntimeStatusesNames,
    VoidForgerToggleAutoExecutionActionTypesNames
)


class VoidForgerView_AutoRunVoidForger(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - TOGGLE_ACTIVATE_AND_DEACTIVATE_VOIDFORGER
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.TOGGLE_ACTIVATE_AND_DEACTIVATE_VOIDFORGER
        ):
            messages.error(
                self.request,
                "You do not have permission to toggle the activation status of VoidForger."
            )
            return redirect('voidforger:configuration')
        ##############################

        try:
            voidforger_id = kwargs.get('voidforger_id')

            voidforger = VoidForger.objects.get(
                id=voidforger_id
            )

            if voidforger.runtime_status == VoidForgerRuntimeStatusesNames.PAUSED:
                voidforger.runtime_status = VoidForgerRuntimeStatusesNames.ACTIVE

            elif voidforger.runtime_status == VoidForgerRuntimeStatusesNames.ACTIVE:
                voidforger.runtime_status = VoidForgerRuntimeStatusesNames.PAUSED

                voidforger.last_auto_execution_started_at = None
                voidforger.last_auto_execution_ended_at = None

                # Reset the current cycle if the VoidForger is paused.
                voidforger.auto_run_current_cycle = 0

            elif voidforger.runtime_status == VoidForgerRuntimeStatusesNames.WORKING:
                messages.error(
                    self.request,
                    "VoidForger is currently working on a task. Please wait for it to finish before toggling."
                )

                return redirect('voidforger:configuration')

            else:
                messages.error(
                    self.request,
                    "VoidForger status is invalid."
                )

                return redirect('voidforger:configuration')

            voidforger.save()

            new_status = voidforger.runtime_status

            if new_status == VoidForgerRuntimeStatusesNames.ACTIVE:
                action_type = VoidForgerToggleAutoExecutionActionTypesNames.ACTIVATED

                metadata = {
                    "message": "VoidForger activation has been triggered by manual user interference. Activated VoidForger auto-execution pipeline."
                }

            elif new_status == VoidForgerRuntimeStatusesNames.PAUSED:
                action_type = VoidForgerToggleAutoExecutionActionTypesNames.PAUSED

                metadata = {
                    "message": "VoidForger de-activation has been triggered by manual user interference. Paused VoidForger auto-execution pipeline."
                }

            else:
                messages.error(
                    self.request,
                    "VoidForger action type is invalid."
                )

                return redirect('voidforger:configuration')

            VoidForgerToggleAutoExecutionLog.objects.create(
                voidforger=voidforger,
                action_type=action_type,
                metadata=metadata,
                responsible_user=self.request.user
            )

        except Exception as e:
            messages.error(
                self.request,
                "VoidForger not found."
            )

            return redirect('voidforger:configuration')

        messages.success(
            self.request,
            "VoidForger activation status toggled to [" + new_status + "]."
        )

        return redirect('voidforger:configuration')
