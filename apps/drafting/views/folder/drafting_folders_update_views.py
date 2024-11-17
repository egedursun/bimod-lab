#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_folders_update_views.py
#  Last Modified: 2024-10-14 18:45:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:45:39
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
from apps.drafting.models import DraftingFolder
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DraftingView_FolderUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        folder_id = self.kwargs['folder_id']

        try:
            folder = get_object_or_404(DraftingFolder, id=folder_id)
            organizations = Organization.objects.filter(users__in=[self.request.user])
            context['folder'] = folder
            context['organizations'] = organizations
        except Exception as e:
            logger.error(f"Error getting Drafting Folder: {e}")
            messages.error(self.request, 'An error occurred while getting Drafting Folder.')
            return context

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_DRAFTING_FOLDERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_DRAFTING_FOLDERS):
            messages.error(self.request, "You do not have permission to update Drafting Folders.")
            return redirect('drafting:folders_list')
        ##############################

        folder_id = self.kwargs['folder_id']
        folder = get_object_or_404(DraftingFolder, id=folder_id)

        try:
            folder.name = request.POST.get('name')
            folder.description = request.POST.get('description', '')
            folder.meta_context_instructions = request.POST.get('meta_context_instructions', '')
            organization_id = request.POST.get('organization')
            if organization_id:
                folder.organization_id = organization_id
            folder.save()
        except Exception as e:
            logger.error(f"Error updating Drafting Folder: {e}")
            messages.error(self.request, 'An error occurred while updating Drafting Folder.')
            return redirect('drafting:folders_list')

        logger.info(f"Drafting Folder was updated by User: {request.user.id}.")
        return redirect('drafting:folders_list')
