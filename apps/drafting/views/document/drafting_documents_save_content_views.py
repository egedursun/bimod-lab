#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_documents_save_content_views.py
#  Last Modified: 2024-10-15 21:18:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 21:18:31
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.drafting.models import DraftingDocument
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)


class DraftingView_SaveContent(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_DRAFTING_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_DRAFTING_DOCUMENTS):
            messages.error(self.request, "You do not have permission to update Drafting Documents.")
            return redirect('drafting:documents_list', folder_id=self.kwargs['folder_id'])
        ##############################

        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']
        document = get_object_or_404(DraftingDocument, id=document_id)
        document_content = request.POST.get('draft_text')
        if document_content:
            document.document_content_json_quill = document_content
            document.save()
        logger.info(f"Drafting Document {document.document_title} was updated.")
        return redirect('drafting:documents_detail', folder_id=folder_id, document_id=document_id)
