#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_ml_item_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelItemUpdateView(LoginRequiredMixin, TemplateView):
    """
    Displays and updates the details of a specific machine learning model item.

    This view allows users with the appropriate permissions to view and update the details of an ML model item.

    Methods:
        get_context_data(self, **kwargs): Retrieves the ML model item details and adds them to the context.
        post(self, request, *args, **kwargs): Handles the update of the ML model item's details.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to update ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        return self.render_to_response(self.get_context_data(**kwargs))
