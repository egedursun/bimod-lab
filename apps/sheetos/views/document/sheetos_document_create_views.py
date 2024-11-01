#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_document_create_views.py
#  Last Modified: 2024-10-31 19:23:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:30:13
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
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.sheetos.models import SheetosFolder, SheetosDocument
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SheetosView_DocumentCreate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_SHEETOS_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SHEETOS_DOCUMENTS):
            messages.error(self.request, "You do not have permission to add Sheetos Documents.")
            return redirect('sheetos:documents_list', folder_id=self.kwargs['folder_id'])
        ##############################

        folder_id = self.kwargs['folder_id']
        folder = get_object_or_404(SheetosFolder, id=folder_id)
        document = SheetosDocument.objects.create(
            organization=folder.organization,
            document_folder=folder,
            document_title=request.POST.get('document_title'),
            copilot_assistant_id=request.POST.get('copilot_assistant'),
            context_instructions=request.POST.get('context_instructions', ''),
            target_audience=request.POST.get('target_audience', ''),
            tone=request.POST.get('tone', ''),
            created_by_user=request.user,
            last_updated_by_user=request.user
        )
        logger.info(f"Sheetos Document {document.document_title} was created.")
        return redirect('sheetos:documents_detail', folder_id=folder.id, document_id=document.id)

