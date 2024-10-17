#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_ml_models_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_ml_models.models import DataSourceMLModelItem
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)



class SettingsView_DeleteAllMLModels(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_ml_models = DataSourceMLModelItem.objects.filter(
            ml_model_base__assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL ML MODELS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ML MODELS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to delete ML model files.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for ml_model in user_ml_models:
                ml_model.delete()
            messages.success(request, "All ML models associated with your account have been deleted.")
            logger.info(f"All ML models associated with User: {user.id} have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting ML models: {e}")
            logger.error(f"Error deleting ML models: {e}")
        return redirect('user_settings:settings')
