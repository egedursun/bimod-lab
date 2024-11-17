#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_document_update_views.py
#  Last Modified: 2024-10-31 19:23:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:23:36
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
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.sheetos.models import SheetosFolder, SheetosDocument
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SheetosView_DocumentUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']
        folder = get_object_or_404(SheetosFolder, id=folder_id)
        document = get_object_or_404(SheetosDocument, id=document_id, document_folder=folder)
        available_folders = SheetosFolder.objects.filter(organization=folder.organization)
        assistants = Assistant.objects.filter(organization=folder.organization)
        context['folder'] = folder
        context['document'] = document
        context['available_folders'] = available_folders
        context['assistants'] = assistants
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_SHEETOS_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SHEETOS_DOCUMENTS):
            messages.error(self.request, "You do not have permission to update Sheetos Documents.")
            return redirect('sheetos:documents_list', folder_id=self.kwargs['folder_id'])
        ##############################

        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']
        folder = get_object_or_404(SheetosFolder, id=folder_id)

        try:
            document = get_object_or_404(SheetosDocument, id=document_id, document_folder=folder)
            document.document_title = request.POST.get('document_title')
            document.copilot_assistant_id = request.POST.get('copilot_assistant')
            document.document_folder_id = request.POST.get('document_folder')
            document.context_instructions = request.POST.get('context_instructions', '')
            document.target_audience = request.POST.get('target_audience', '')
            document.tone = request.POST.get('tone', '')
            document.last_updated_by_user = request.user
            document.save()
        except Exception as e:
            messages.error(request, f"An error occurred while updating the Sheetos Document: {str(e)}")
            return redirect('sheetos:documents_list', folder_id=folder_id)

        logger.info(f"Sheetos Document {document.document_title} was updated.")
        return redirect('sheetos:documents_list', folder_id=folder_id)
