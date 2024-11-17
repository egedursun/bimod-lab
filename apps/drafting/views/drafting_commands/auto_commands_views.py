#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auto_commands.py
#  Last Modified: 2024-10-15 23:18:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 23:18:01
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
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.drafting.drafting_executor import DraftingExecutionManager
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.drafting.models import DraftingDocument
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class DraftingView_GenerateViaAutoCommand(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        document_id = request.POST.get('document_id')
        document = get_object_or_404(DraftingDocument, pk=document_id)

        ##############################
        # PERMISSION CHECK FOR - UPDATE_DRAFTING_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_DRAFTING_DOCUMENTS):
            messages.error(self.request, "You do not have permission to update Drafting Documents.")
            return redirect('drafting:documents_detail',
                            folder_id=document.document_folder.id, document_id=document_id)
        ##############################

        try:
            xc = DraftingExecutionManager(drafting_document=document)
            response_json = xc.execute_auto_command()
        except Exception as e:
            logger.error(f"Error executing Auto Command for Drafting Document: {e}")
            messages.error(self.request, 'An error occurred while executing Auto Command.')
            return redirect('drafting:documents_detail',
                            folder_id=document.document_folder.id, document_id=document_id)

        logger.info(f"Auto Command was executed for Drafting Document: {document.id}.")
        return JsonResponse(response_json)
