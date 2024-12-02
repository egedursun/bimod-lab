#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_ml_storage_views.py
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
from apps.datasource_ml_models.forms import DataSourceMLModelConnectionForm
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_ML_STORAGES_PER_ASSISTANT
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class MLModelView_ManagerCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, context)
        context['form'] = DataSourceMLModelConnectionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DataSourceMLModelConnectionForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to create ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        if form.is_valid():

            assistant = form.cleaned_data['assistant']

            # check the number of ML model storage connections assistant has
            n_ml_storages = assistant.datasourcemlmodelconnection_set.count()
            if n_ml_storages > MAX_ML_STORAGES_PER_ASSISTANT:
                messages.error(request,
                               f'Assistant has reached the maximum number of ML storage connections ({MAX_ML_STORAGES_PER_ASSISTANT}).')
                return redirect('datasource_ml_models:list')

            conn = form.save(commit=False)
            conn.created_by_user = request.user
            conn.save()
            logger.info(f"ML Model Connection created: {conn}")
            messages.success(request, 'ML Model Connection created successfully.')
            return redirect('datasource_ml_models:list')
        else:
            logger.error('There was an error creating the ML Model Connection.')
            messages.error(request, 'There was an error creating the ML Model Connection.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
