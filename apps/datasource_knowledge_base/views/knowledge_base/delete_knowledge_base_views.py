#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_knowledge_base_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:45
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
#  File: delete_knowledge_base_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:45:44
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
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DocumentKnowledgeBaseDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of a document knowledge base connection.

    This view allows users with the appropriate permissions to delete a knowledge base connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes the knowledge base connection if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the knowledge base connections that belong to the user's assistants.
    """

    model = DocumentKnowledgeBaseConnection
    success_url = '/app/datasource_knowledge_base/list/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['knowledge_base'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_KNOWLEDGE_BASES):
            messages.error(self.request, "You do not have permission to delete Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

    def get_queryset(self):
        context_user = self.request.user
        return DocumentKnowledgeBaseConnection.objects.filter(assistant__organization__users__in=[context_user])
