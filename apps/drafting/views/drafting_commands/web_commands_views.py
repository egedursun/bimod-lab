#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: web_commands.py
#  Last Modified: 2024-10-15 23:18:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 23:18:49
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
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.drafting.drafting_executor import DraftingExecutionManager
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.drafting.models import DraftingDocument
from apps.user_permissions.utils import PermissionNames


class DraftingView_GenerateViaWebCommand(LoginRequiredMixin, View):

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

        command = request.POST.get('command')
        xc = DraftingExecutionManager(drafting_document=document)
        response_json = xc.execute_web_command(command=command)
        return JsonResponse(response_json)
