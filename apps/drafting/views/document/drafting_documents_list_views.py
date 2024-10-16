#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: drafting_documents_list_views.py
#  Last Modified: 2024-10-14 14:07:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:54:06
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.drafting.models import DraftingFolder, DraftingDocument
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DraftingView_DocumentList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_DRAFTING_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_DRAFTING_DOCUMENTS):
            messages.error(self.request, "You do not have permission to list Drafting Documents.")
            return context
        ##############################

        folder_id = self.kwargs['folder_id']
        folder = get_object_or_404(DraftingFolder, id=folder_id)
        documents = DraftingDocument.objects.filter(document_folder=folder)
        assistants = Assistant.objects.filter(organization=folder.organization)
        context['folder'] = folder
        context['documents'] = documents
        context['assistants'] = assistants
        return context


