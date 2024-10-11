#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_code_base_storage_views.py
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_codebase.forms import CodeRepositoryStorageForm
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.datasource_codebase.utils import KNOWLEDGE_BASE_SYSTEMS, VECTORIZERS
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CodeBaseView_StorageUpdate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        vector_store = get_object_or_404(CodeRepositoryStorageConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_orgs = context_user.organizations.all()
        agents_of_orgs = Assistant.objects.filter(organization__in=user_orgs)
        context['assistants'] = agents_of_orgs
        context['connection'] = vector_store
        context['form'] = CodeRepositoryStorageForm(instance=vector_store)
        return context

    def post(self, request, *args, **kwargs):
        vector_store = get_object_or_404(CodeRepositoryStorageConnection, pk=kwargs['pk'])

        ##############################
        # PERMISSION CHECK FOR - UPDATE_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_CODE_BASE):
            messages.error(self.request, "You do not have permission to update code base storages.")
            return redirect('datasource_codebase:list')
        ##############################

        form = CodeRepositoryStorageForm(request.POST, instance=vector_store)
        if form.is_valid():
            form.save()
            messages.success(request, "Code Base Storage updated successfully.")
            return redirect('datasource_codebase:list')
        else:
            messages.error(request, "Error updating Code Base Storage. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
