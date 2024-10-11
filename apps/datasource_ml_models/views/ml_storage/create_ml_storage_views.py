#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_ml_models.forms import DataSourceMLModelConnectionForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


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
            conn = form.save(commit=False)
            conn.created_by_user = request.user
            conn.save()
            messages.success(request, 'ML Model Connection created successfully.')
            return redirect('datasource_ml_models:list')
        else:
            messages.error(request, 'There was an error creating the ML Model Connection.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
