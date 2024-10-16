#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: drafting_documents_update_views.py
#  Last Modified: 2024-10-15 20:05:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 20:05:05
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


class DraftingView_DocumentUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']
        folder = get_object_or_404(DraftingFolder, id=folder_id)
        document = get_object_or_404(DraftingDocument, id=document_id, document_folder=folder)
        available_folders = DraftingFolder.objects.filter(organization=folder.organization)
        assistants = Assistant.objects.filter(organization=folder.organization)
        context['folder'] = folder
        context['document'] = document
        context['available_folders'] = available_folders
        context['assistants'] = assistants
        return context

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
        folder = get_object_or_404(DraftingFolder, id=folder_id)
        document = get_object_or_404(DraftingDocument, id=document_id, document_folder=folder)
        document.document_title = request.POST.get('document_title')
        document.copilot_assistant_id = request.POST.get('copilot_assistant')
        document.document_folder_id = request.POST.get('document_folder')
        document.context_instructions = request.POST.get('context_instructions', '')
        document.target_audience = request.POST.get('target_audience', '')
        document.tone = request.POST.get('tone', '')
        document.last_updated_by_user = request.user
        document.save()
        return redirect('drafting:documents_list', folder_id=folder_id)
