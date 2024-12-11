#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_codebase.models import (
    CodeBaseRepository
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class CodeBaseView_RepositoryDeleteAll(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        vs_id = kwargs.get('kb_id')

        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_CODE_REPOSITORY
        ):
            messages.error(self.request, "You do not have permission to delete code repositories.")
            return redirect('datasource_codebase:list_repositories')
        ##############################

        try:
            CodeBaseRepository.objects.filter(
                knowledge_base_id=vs_id
            ).delete()

        except Exception as e:
            logger.error(f"User: {request.user} - Code Repository - Delete All Error: {e}")
            messages.error(request, 'An error occurred while deleting all repositories.')

            return redirect('datasource_codebase:list_repositories')

        logger.info(
            f"[CodeBaseView_RepositoryDeleteAll] All repositories in the selected knowledge base have been deleted.")

        messages.success(request, 'All repositories in the selected knowledge base have been deleted successfully.')

        return redirect('datasource_codebase:list_repositories')
