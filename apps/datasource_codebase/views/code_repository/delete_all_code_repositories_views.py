#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_all_code_repositories_views.py
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
from apps.datasource_codebase.models import CodeBaseRepository
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteAllRepositoriesView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        knowledge_base_id = kwargs.get('kb_id')
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to delete code repositories.")
            return redirect('datasource_codebase:list_repositories')
        ##############################

        CodeBaseRepository.objects.filter(knowledge_base_id=knowledge_base_id).delete()
        messages.success(request, 'All repositories in the selected knowledge base have been deleted successfully.')
        print(
            '[DeleteAllRepositoriesView.post] All repositories in the selected knowledge base have been deleted successfully.')
        return redirect('datasource_codebase:list_repositories')
