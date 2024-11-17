#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ai_commands_views.py
#  Last Modified: 2024-10-17 16:15:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:27:25
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

from apps.core.sheetos.sheetos_executor import SheetosExecutionManager
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.sheetos.models import SheetosDocument
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SheetosView_GenerateViaAICommand(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        document_id = request.POST.get('document_id')
        document = get_object_or_404(SheetosDocument, pk=document_id)

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SHEETOS_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SHEETOS_DOCUMENTS):
            messages.error(self.request, "You do not have permission to update Sheetos Documents.")
            return redirect('sheetos:documents_detail',
                            folder_id=document.document_folder.id, document_id=document_id)
        ##############################

        try:
            command = request.POST.get('command')
            xc = SheetosExecutionManager(sheetos_document=document)
            response_json = xc.execute_ai_command(command=command)
        except Exception as e:
            messages.error(request, f"An error occurred while executing the AI Command: {str(e)}")
            return redirect('sheetos:documents_detail',
                            folder_id=document.document_folder.id, document_id=document_id)

        logger.info(f"AI Command was executed for Sheetos Document: {document.id}.")
        return JsonResponse(response_json)
