#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_folders_list_views.py
#  Last Modified: 2024-10-14 18:46:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:46:52
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
from apps.drafting.models import DraftingFolder
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class DraftingView_FolderList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_DRAFTING_FOLDERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_DRAFTING_FOLDERS):
            messages.error(self.request, "You do not have permission to list Drafting Folders.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        org_folders = []
        for org in user_orgs:
            folders = DraftingFolder.objects.filter(organization=org)
            org_folders.append({
                'organization': org,
                'folders': folders
            })
        context['org_folders'] = org_folders
        context['organizations'] = user_orgs
        logger.info(f"Drafting Folders were listed for User: {self.request.user.id}.")
        return context
