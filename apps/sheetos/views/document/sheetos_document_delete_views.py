#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_document_delete_views.py
#  Last Modified: 2024-10-31 19:23:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:23:43
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
    redirect,
    get_object_or_404
)

from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.sheetos.models import (
    SheetosDocument
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SheetosView_DocumentDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_SHEETOS_DOCUMENTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_SHEETOS_DOCUMENTS
        ):
            messages.error(self.request, "You do not have permission to delete Sheetos Documents.")

        return redirect(
            'sheetos:documents_list',
            folder_id=self.kwargs['folder_id']
        )
        ##############################

        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']

        document = get_object_or_404(
            SheetosDocument,
            id=document_id
        )

        try:
            document.delete()

        except Exception as e:
            messages.error(request, f"An error occurred while deleting the Sheetos Document: {str(e)}")

            return redirect(
                'sheetos:documents_list',
                folder_id=folder_id
            )

        logger.info(f"Sheetos Document {document.document_title} was deleted.")

        return redirect(
            'sheetos:documents_list',
            folder_id=folder_id
        )
