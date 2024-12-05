#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_export_leanmod_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportLeanModView_Delete(LoginRequiredMixin, DeleteView):
    model = ExportLeanmodAssistantAPI
    success_url = 'export_leanmods:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_EXPORT_LEANMOD
        ):
            messages.error(self.request, "You do not have permission to delete Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        exp_leanmod = get_object_or_404(ExportLeanmodAssistantAPI, id=self.kwargs['pk'])
        exp_leanmod.delete()

        success_message = "Export LeanMod Assistant deleted successfully."
        org = exp_leanmod.lean_assistant.organization
        org.exported_leanmods.remove(exp_leanmod)

        org.save()

        logger.info(f"Export LeanMod Assistant was deleted by User: {request.user.id}.")
        messages.success(request, success_message)

        return redirect(self.success_url)
