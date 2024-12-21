#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_ml_models_views.py
#  Last Modified: 2024-11-08 14:48:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-08 14:48:16
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
import uuid

import requests
from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)
from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection,
    DataSourceMLModelItem
)

from apps.ml_model_store.models import (
    MLModelIntegration
)

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_ML_MODELS_PER_STORAGE
)

logger = logging.getLogger(__name__)


class MLModelStoreView_IntegrateMLModel(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - INTEGRATE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.INTEGRATE_ML_MODEL_FILES
        ):
            messages.error(self.request, "You do not have permission to integrate ML Model files.")

            return redirect('ml_model_store:list')
        ##############################

        item_id = kwargs['pk']

        if not item_id:
            messages.error(self.request, "ML Model Integration ID is missing.")

            logger.error("ML Model Integration ID is missing.")

            return redirect('ml_model_store:list')

        integration_boilerplate:MLModelIntegration = MLModelIntegration.objects.get(
            id=item_id
        )

        if not integration_boilerplate:
            messages.error(self.request, "ML Model Integration ID is invalid.")

            logger.error("ML Model Integration ID is invalid.")

            return redirect('ml_model_store:list')

        connection_id = request.POST.get('connection_id')

        if not connection_id:
            messages.error(self.request, "Connection ID is missing.")

            logger.error("Connection ID is missing.")

            return redirect('ml_model_store:list')

        connection_storage:DataSourceMLModelConnection = DataSourceMLModelConnection.objects.get(
            id=connection_id
        )

        if not connection_storage:
            messages.error(self.request, "Connection ID is invalid.")

            logger.error("Connection ID is invalid.")

            return redirect('ml_model_store:list')

        object_url = integration_boilerplate.model_download_url

        if not object_url:
            messages.error(self.request, "Model URL is missing.")

            logger.error("Model URL is missing.")

            return redirect('ml_model_store:list')

        try:
            response = requests.get(
                object_url
            )

            if response.status_code != 200:
                messages.error(self.request, "Model URL is invalid.")

                logger.error("Model URL is invalid.")

                return redirect('ml_model_store:list')

            model_file = response.content

        except Exception as e:
            messages.error(self.request, "Model URL is invalid.")

            logger.error("Model URL is invalid.")

            return redirect('ml_model_store:list')

        model_item_name = f"{integration_boilerplate.name}-{str(uuid.uuid4()).replace('-', '')}"
        model_item_description = integration_boilerplate.description
        model_item_file_bytes = model_file
        model_item_file_size = len(model_file)

        n_ml_items = connection_storage.items.count()

        if n_ml_items > MAX_ML_MODELS_PER_STORAGE:
            messages.error(
                request,
                f'Assistant has reached the maximum number of ML items in the storage ({MAX_ML_MODELS_PER_STORAGE}).'
            )

            return redirect('datasource_ml_models:item_create')

        try:
            model_item = DataSourceMLModelItem.objects.create(
                ml_model_base=connection_storage,
                ml_model_name=model_item_name,
                description=model_item_description,
                file_bytes=model_item_file_bytes,
                ml_model_size=model_item_file_size,
                created_by_user=request.user
            )

            logger.info(f"ML Model Item integrated successfully: {model_item}")

            messages.success(request, 'ML Model Item integrated successfully.')

            return redirect('ml_model_store:list')

        except Exception as e:
            logger.error(f"An error occurred while integrating ML Model Item: {e}")

            messages.error(request, 'An error occurred while integrating ML Model Item.')

            return redirect('ml_model_store:list')
