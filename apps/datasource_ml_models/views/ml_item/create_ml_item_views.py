#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
from apps.assistants.models import Assistant
from apps.datasource_ml_models.forms import DataSourceMLModelItemForm
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MLModelView_ItemCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_orgs = context_user.organizations.all()
        user_agents = Assistant.objects.filter(organization__in=user_orgs)
        ml_managers = DataSourceMLModelConnection.objects.filter(assistant__in=user_agents).all()
        context['ml_model_connections'] = ml_managers
        context['form'] = DataSourceMLModelItemForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DataSourceMLModelItemForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to add ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        if form.is_valid():
            ml_model_item = form.save(commit=False)
            uploaded_file = request.FILES['file']
            ml_model_item.file_bytes = uploaded_file.read()
            ml_model_item.ml_model_size = uploaded_file.size
            ml_model_item.created_by_user = request.user
            ml_model_item.save()
            messages.success(request, 'ML Model Item uploaded successfully.')
            return redirect('datasource_ml_models:item_list')
        else:
            messages.error(request, 'There was an error uploading the ML Model Item.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
