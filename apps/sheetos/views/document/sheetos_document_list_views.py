#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_document_list_views.py
#  Last Modified: 2024-10-31 19:23:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:23:28
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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.sheetos.models import SheetosFolder, SheetosDocument
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SheetosView_DocumentList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SHEETOS_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SHEETOS_DOCUMENTS):
            messages.error(self.request, "You do not have permission to list Sheetos Documents.")
            return context
        ##############################

        folder_id = self.kwargs['folder_id']
        folder = get_object_or_404(SheetosFolder, id=folder_id)
        documents = SheetosDocument.objects.filter(document_folder=folder)
        assistants = Assistant.objects.filter(organization=folder.organization)
        paginator = Paginator(documents, 10)
        page = self.request.GET.get('page')
        try:
            documents = paginator.page(page)
        except PageNotAnInteger:
            documents = paginator.page(1)
        except EmptyPage:
            documents = paginator.page(paginator.num_pages)
        context['folder'] = folder
        context['documents'] = documents
        context['assistants'] = assistants
        logger.info(f"Sheetos Documents in Folder {folder.name} were listed.")
        return context
