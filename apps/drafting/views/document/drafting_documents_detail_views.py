#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: drafting_documents_create_update_views.py
#  Last Modified: 2024-10-14 14:03:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 14:03:22
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.drafting.models import DraftingDocument
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DraftingView_DocumentDetail(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_DRAFTING_DOCUMENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_DRAFTING_DOCUMENTS):
            messages.error(self.request, "You do not have permission to list Drafting Documents.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        document_id = self.kwargs.get('document_id')
        document = DraftingDocument.objects.get(id=document_id)
        context['document'] = document
        context['folder'] = document.document_folder
        content = document.document_content_json_quill
        context['content'] = content
        return context
