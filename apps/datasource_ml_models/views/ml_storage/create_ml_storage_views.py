#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_ml_storage_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: create_ml_storage_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:48:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_ml_models.forms import DataSourceMLModelConnectionForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelConnectionCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new machine learning model connections.

    This view displays a form for creating a new ML model connection. Upon submission, it validates the input, checks user permissions, and saves the new connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including the form for creating an ML model connection.
        post(self, request, *args, **kwargs): Handles form submission and ML model connection creation, including permission checks and validation.
    """

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
            ml_model_connection = form.save(commit=False)
            ml_model_connection.created_by_user = request.user
            ml_model_connection.save()
            messages.success(request, 'ML Model Connection created successfully.')
            print('[DataSourceMLModelConnectionCreateView.post] ML Model Connection created successfully.')
            return redirect('datasource_ml_models:list')
        else:
            messages.error(request, 'There was an error creating the ML Model Connection.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
