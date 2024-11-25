#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_export_voidforger_views.py
#  Last Modified: 2024-11-24 21:36:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 22:06:12
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

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.export_voidforger.models import ExportVoidForgerAPI
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportVoidForgerView_Delete(LoginRequiredMixin, DeleteView):
    model = ExportVoidForgerAPI
    success_url = 'export_voidforger:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPORT_VOIDFORGER
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_EXPORT_VOIDFORGER
        ):
            messages.error(self.request, "You do not have permission to delete Export VoidForger APIs.")
            return redirect('export_voidforger:list')
        ##############################

        exp_agent = get_object_or_404(ExportVoidForgerAPI, id=self.kwargs['pk'])
        exp_agent.delete()
        success_message = "Export VoidForger deleted successfully."

        org = exp_agent.voidforger.llm_model.organization
        org.exported_voidforgers.remove(exp_agent)
        org.save()

        logger.info(f"Export VoidForger was deleted by User: {request.user.id}.")
        messages.success(request, success_message)
        return redirect(self.success_url)
