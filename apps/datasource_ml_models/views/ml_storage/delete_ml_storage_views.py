#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_ml_storage_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    redirect,
    get_object_or_404
)

from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MLModelView_ManagerDelete(LoginRequiredMixin, DeleteView):
    model = DataSourceMLModelConnection
    success_url = 'datasource_ml_models:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_ML_MODEL_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to delete ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        conn = get_object_or_404(
            DataSourceMLModelConnection,
            id=kwargs['pk']
        )

        try:
            conn.delete()

        except Exception as e:
            logger.error(f"Error deleting ML Model Connection: {e}")
            messages.error(self.request, 'An error occurred while deleting ML Model Connection.')

            return redirect(self.success_url)

        logger.info(f"ML Model Connection deleted: {conn}")

        return redirect(self.success_url)

    def get_queryset(self):
        user = self.request.user

        return DataSourceMLModelConnection.objects.filter(
            assistant__organization__in=user.organizations.all()
        )
