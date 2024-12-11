#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_ml_item_views.py
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

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant

from apps.datasource_ml_models.forms import (
    DataSourceMLModelItemForm
)

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_ML_MODELS_PER_STORAGE
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MLModelView_ItemCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            user_agents = Assistant.objects.filter(
                organization__in=user_orgs
            )

            ml_managers = DataSourceMLModelConnection.objects.filter(
                assistant__in=user_agents
            ).all()

            context['ml_model_connections'] = ml_managers
            context['form'] = DataSourceMLModelItemForm()

        except Exception as e:
            logger.error(f"User: {context_user} - ML Model Item - Create Error: {e}")
            messages.error(self.request, 'An error occurred while creating ML Model Item.')

            return context

        return context

    def post(self, request, *args, **kwargs):
        form = DataSourceMLModelItemForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_ML_MODEL_FILES
        ):
            messages.error(self.request, "You do not have permission to add ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        if form.is_valid():

            ml_model_base = form.cleaned_data['ml_model_base']

            n_ml_items = ml_model_base.items.count()

            if n_ml_items > MAX_ML_MODELS_PER_STORAGE:
                messages.error(
                    request,
                    f'Assistant has reached the maximum number of ML items in the storage ({MAX_ML_MODELS_PER_STORAGE}).'
                )

                return redirect('datasource_ml_models:item_create')

            ml_model_item = form.save(commit=False)
            uploaded_file = request.FILES['file']

            ml_model_item.file_bytes = uploaded_file.read()
            ml_model_item.ml_model_size = uploaded_file.size
            ml_model_item.created_by_user = request.user

            ml_model_item.save()

            logger.info(f'ML Model Item uploaded: {ml_model_item}')
            messages.success(request, 'ML Model Item uploaded successfully.')

            return redirect('datasource_ml_models:item_list')

        else:
            logger.error('There was an error uploading the ML Model Item.')
            messages.error(request, 'There was an error uploading the ML Model Item.')

            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)
