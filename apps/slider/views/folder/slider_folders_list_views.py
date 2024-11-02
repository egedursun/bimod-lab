#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: slider_folders_list_views.py
#  Last Modified: 2024-11-01 05:25:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 20:06:35
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
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.slider.models import SliderFolder
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SliderView_FolderList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SLIDER_FOLDERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SLIDER_FOLDERS):
            messages.error(self.request, "You do not have permission to list Slider Folders.")
            return context
        ##############################

        # Get organizations and paginate folders for each
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        org_folders = []
        for org in user_orgs:
            folders = SliderFolder.objects.filter(organization=org)
            paginator = Paginator(folders, 10)
            page_number = self.request.GET.get(f'page_{org.id}', 1)
            page_obj = paginator.get_page(page_number)
            org_folders.append({
                'organization': org,
                'page_obj': page_obj,
            })
        context['org_folders'] = org_folders
        context['organizations'] = user_orgs
        logger.info(f"Slider Folders were listed for User: {self.request.user.id}.")
        return context
