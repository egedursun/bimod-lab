#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_folder_create_views.py
#  Last Modified: 2024-10-31 19:24:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:24:51
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
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.sheetos.models import SheetosFolder
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SheetosView_FolderCreate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_SHEETOS_FOLDERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SHEETOS_FOLDERS):
            messages.error(self.request, "You do not have permission to add Sheetos Folders.")
            return redirect('sheetos:folders_list')
        ##############################

        organization_id = request.POST.get('organization')
        folder_name = request.POST.get('name')
        description = request.POST.get('description', '')
        meta_context_instructions = request.POST.get('meta_context_instructions', '')

        if organization_id and folder_name:
            organization = Organization.objects.get(id=organization_id)
            SheetosFolder.objects.create(
                organization=organization, name=folder_name, description=description,
                meta_context_instructions=meta_context_instructions, created_by_user=request.user
            )
        logger.info(f"Sheetos Folder was created by User: {request.user.id}.")
        return redirect('sheetos:folders_list')
