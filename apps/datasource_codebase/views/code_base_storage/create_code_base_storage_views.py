#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_code_base_storage_views.py
#  Last Modified: 2024-10-05 01:39:47
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
from apps.assistants.models import Assistant
from apps.datasource_codebase.forms import CodeRepositoryStorageForm
from apps.datasource_codebase.utils import KNOWLEDGE_BASE_SYSTEMS, VECTORIZERS
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CodeBaseStorageCreateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['form'] = CodeRepositoryStorageForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CodeRepositoryStorageForm(request.POST)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_CODE_BASE):
            messages.error(self.request, "You do not have permission to add code base storages.")
            return redirect('datasource_codebase:list')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "Code Base Storage created successfully.")
            print('[CodeBaseStorageCreateView.post] Code Base Storage created successfully.')
            return redirect('datasource_codebase:list')
        else:
            messages.error(request, "Error creating Code Base Storage. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
