#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_documents_create_views.py
#  Last Modified: 2024-10-14 18:48:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:48:19
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.drafting.models import (
    DraftingFolder,
    DraftingDocument
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class DraftingView_DocumentCreate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_DRAFTING_DOCUMENTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_DRAFTING_DOCUMENTS
        ):
            messages.error(self.request, "You do not have permission to add Drafting Documents.")
            return redirect('drafting:documents_list', folder_id=self.kwargs['folder_id'])
        ##############################

        folder_id = self.kwargs['folder_id']

        try:
            folder = get_object_or_404(
                DraftingFolder,
                id=folder_id
            )

            document = DraftingDocument.objects.create(
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

        except Exception as e:
            logger.error(f"Error creating Drafting Document: {e}")

            messages.error(self.request, 'An error occurred while creating Drafting Document.')

            return redirect(
                'drafting:documents_list',
                folder_id=folder_id
            )

        logger.info(f"Drafting Document {document.document_title} was created.")

        return redirect(
            'drafting:documents_detail',
            folder_id=folder.id,
            document_id=document.id
        )
