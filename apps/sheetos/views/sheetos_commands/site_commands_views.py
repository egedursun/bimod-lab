#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: site_commands_views.py
#  Last Modified: 2024-12-09 21:26:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 21:26:02
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

from django.http import JsonResponse

from django.shortcuts import (
    redirect,
    get_object_or_404
)

from django.views import View

from apps.core.sheetos.sheetos_executor import (
    SheetosExecutionManager
)

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


class SheetosView_GenerateViaSiteCommand(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        document_id = request.POST.get('document_id')

        document = get_object_or_404(
            SheetosDocument,
            pk=document_id
        )

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SHEETOS_DOCUMENTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_SHEETOS_DOCUMENTS
        ):
            messages.error(self.request, "You do not have permission to update Sheetos Documents.")

            return redirect(
                'sheetos:documents_detail',
                folder_id=document.document_folder.id,
                document_id=document_id
            )
        ##############################

        try:
            command = request.POST.get('command')

            xc = SheetosExecutionManager(
                sheetos_document=document
            )

            response_json = xc.execute_site_command(
                command=command
            )

        except Exception as e:
            logger.error(f"Error executing Site Command for Sheetos Document: {e}")
            messages.error(self.request, 'An error occurred while executing Site Command.')

            return redirect(
                'sheetos:documents_detail',
                folder_id=document.document_folder.id,
                document_id=document_id
            )

        logger.info(f"Site Command was executed for Sheetos Document: {document.id}.")

        return JsonResponse(response_json)
