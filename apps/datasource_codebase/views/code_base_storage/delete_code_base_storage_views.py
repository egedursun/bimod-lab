#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_code_base_storage_views.py
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
#  File: delete_code_base_storage_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:38:58
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
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CodeBaseStorageDeleteView(LoginRequiredMixin, DeleteView):
    model = CodeRepositoryStorageConnection
    success_url = '/app/datasource_codebase/list/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['knowledge_base'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_BASE):
            messages.error(self.request, "You do not have permission to update code base storages.")
            return redirect('datasource_codebase:list')
        ##############################

        print('[CodeBaseStorageDeleteView.post] Code Base Storage deleted successfully.')
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        context_user = self.request.user
        return CodeRepositoryStorageConnection.objects.filter(assistant__organization__users__in=[context_user])
