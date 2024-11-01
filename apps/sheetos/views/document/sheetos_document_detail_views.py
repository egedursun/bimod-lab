#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_document_detail_views.py
#  Last Modified: 2024-10-31 19:23:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:23:52
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.sheetos.models import SheetosDocument
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SheetosView_DocumentDetail(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SHEETOS_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SHEETOS_DOCUMENTS):
            messages.error(self.request, "You do not have permission to list Sheetos Documents.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        document_id = self.kwargs.get('document_id')
        document = SheetosDocument.objects.get(id=document_id)
        context['document'] = document
        context['folder'] = document.document_folder
        content = document.document_content_json_quill
        context['content'] = content
        logger.info(f"Sheetos Document {document.document_title} was viewed.")
        return context
