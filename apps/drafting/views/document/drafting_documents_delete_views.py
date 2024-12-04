#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_documents_delete_views.py
#  Last Modified: 2024-10-14 14:07:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:52:41
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.drafting.models import DraftingDocument
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class DraftingView_DocumentDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_DRAFTING_DOCUMENTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_DRAFTING_DOCUMENTS
        ):
            messages.error(self.request, "You do not have permission to delete Drafting Documents.")
            return redirect('drafting:documents_list', folder_id=self.kwargs['folder_id'])
        ##############################

        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']

        document = get_object_or_404(
            DraftingDocument,
            id=document_id
        )

        try:
            document.delete()

        except Exception as e:
            logger.error(f"Error deleting Drafting Document: {e}")
            messages.error(self.request, 'An error occurred while deleting Drafting Document.')

            return redirect('drafting:documents_list', folder_id=folder_id)

        logger.info(f"Drafting Document {document.document_title} was deleted.")

        return redirect('drafting:documents_list', folder_id=folder_id)
