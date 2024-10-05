#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelConnectionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of a machine learning model connection.

    This view allows users with the appropriate permissions to delete an ML model connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes the ML model connection if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the ML model connections that belong to the user's assistants.
    """

    model = DataSourceMLModelConnection
    success_url = 'datasource_ml_models:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to delete ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        ml_model_connection = get_object_or_404(DataSourceMLModelConnection, id=kwargs['pk'])
        ml_model_connection.delete()
        print('[DataSourceMLModelConnectionDeleteView.post] ML Model Connection deleted successfully.')
        return redirect(self.success_url)

    def get_queryset(self):
        user = self.request.user
        return DataSourceMLModelConnection.objects.filter(assistant__organization__in=user.organizations.all())
