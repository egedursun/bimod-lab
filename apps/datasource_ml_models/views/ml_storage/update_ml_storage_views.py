#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_ml_storage_views.py
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.forms import DataSourceMLModelConnectionForm
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MLModelView_ManagerUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            mgr = DataSourceMLModelConnection.objects.get(id=kwargs['pk'])
            user_orgs = context_user.organizations.all()
            agents = Assistant.objects.filter(organization__in=user_orgs)
            context['form'] = DataSourceMLModelConnectionForm(instance=mgr)
            context['assistants'] = agents
            context['connection'] = mgr
        except Exception as e:
            logger.error(f"User: {context_user} - ML Model Connection - Update Error: {e}")
            messages.error(self.request, 'An error occurred while updating ML Model Connection.')
            return context

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to update ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        mgr = DataSourceMLModelConnection.objects.get(id=kwargs['pk'])
        form = DataSourceMLModelConnectionForm(request.POST, instance=mgr)
        if form.is_valid():
            form.save()
            logger.info(f"ML Model Connection updated: {mgr}")
            messages.success(request, "ML Model Connection updated successfully.")
            return redirect('datasource_ml_models:list')
        else:
            logger.error("Error updating ML Model Connection: " + str(form.errors))
            messages.error(request, "Error updating ML Model Connection: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
