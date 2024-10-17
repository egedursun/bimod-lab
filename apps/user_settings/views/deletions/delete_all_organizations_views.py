#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_organizations_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)


class SettingsView_DeleteAllOrganizations(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_orgs: Organization = Organization.objects.filter(users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL ORGANIZATIONS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ORGANIZATIONS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to delete organizations.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for org in user_orgs:
                org.delete()
            messages.success(request, "All organizations associated with your account have been deleted.")
            logger.info(f"All organizations associated with User: {user.id} have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting organizations: {e}")
            logger.error(f"Error deleting organizations: {e}")
        return redirect('user_settings:settings')
