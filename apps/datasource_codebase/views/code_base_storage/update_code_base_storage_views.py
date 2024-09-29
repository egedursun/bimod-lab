#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: update_code_base_storage_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:39:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_codebase.forms import CodeRepositoryStorageForm
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.datasource_codebase.utils import KNOWLEDGE_BASE_SYSTEMS, VECTORIZERS
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CodeBaseStorageUpdateView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        knowledge_base = get_object_or_404(CodeRepositoryStorageConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['connection'] = knowledge_base
        context['form'] = CodeRepositoryStorageForm(instance=knowledge_base)
        return context

    def post(self, request, *args, **kwargs):
        knowledge_base = get_object_or_404(CodeRepositoryStorageConnection, pk=kwargs['pk'])
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_CODE_BASE):
            messages.error(self.request, "You do not have permission to update code base storages.")
            return redirect('datasource_codebase:list')
        ##############################

        form = CodeRepositoryStorageForm(request.POST, instance=knowledge_base)
        if form.is_valid():
            form.save()
            messages.success(request, "Code Base Storage updated successfully.")
            print('[CodeBaseStorageUpdateView.post] Code Base Storage updated successfully.')
            return redirect('datasource_codebase:list')
        else:
            messages.error(request, "Error updating Code Base Storage. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
