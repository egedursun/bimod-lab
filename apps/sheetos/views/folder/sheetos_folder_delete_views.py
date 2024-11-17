#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_folder_delete_views.py
#  Last Modified: 2024-10-31 19:25:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:25:15
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

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.sheetos.models import SheetosFolder
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SheetosView_FolderDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        folder_id = self.kwargs['folder_id']
        folder = get_object_or_404(SheetosFolder, id=folder_id)
        context['folder'] = folder
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_SHEETOS_FOLDERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SHEETOS_FOLDERS):
            messages.error(self.request, "You do not have permission to delete Sheetos Folders.")
            return redirect('sheetos:folders_list')
        ##############################

        folder_id = self.kwargs['folder_id']
        folder = get_object_or_404(SheetosFolder, id=folder_id)

        try:
            folder.delete()
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the Sheetos Folder: {str(e)}")
            return redirect('sheetos:folders_list')

        logger.info(f"Sheetos Folder was deleted by User: {request.user.id}.")
        return redirect('sheetos:folders_list')
