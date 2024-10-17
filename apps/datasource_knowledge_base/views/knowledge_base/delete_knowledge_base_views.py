#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_knowledge_base_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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
from django.views import View
from django.views.generic import DeleteView, TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class VectorStoreView_Delete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['knowledge_base'] = DocumentKnowledgeBaseConnection.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        vector_store = DocumentKnowledgeBaseConnection.objects.get(pk=self.kwargs['pk'])
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_KNOWLEDGE_BASES):
            messages.error(self.request, "You do not have permission to delete Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        vector_store.delete()
        messages.success(request, "Knowledge Base deleted successfully.")
        return redirect('datasource_knowledge_base:list')
