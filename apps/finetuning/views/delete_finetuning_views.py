#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_finetuning_views.py
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.finetuning.models import FineTunedModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class FineTuningView_Delete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['connection'] = get_object_or_404(
            FineTunedModelConnection,
            id=kwargs['pk'],
            created_by_user=self.request.user
        )

        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_FINETUNING_MODEL
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_FINETUNING_MODEL
        ):
            messages.error(self.request, "You do not have permission to delete Finetuning Model.")
            return redirect('finetuning:list')
        ##############################

        c = get_object_or_404(
            FineTunedModelConnection,
            id=kwargs['pk'],
            created_by_user=request.user
        )

        try:
            c.delete()

        except Exception as e:
            logger.error(f"Error deleting FineTunedModelConnection: {e}")
            messages.error(request, "Error deleting FineTunedModelConnection.")

            return redirect('finetuning:list')

        logger.info(f"FineTuning Model was deleted by User: {context_user.id}.")

        return redirect('finetuning:list')
