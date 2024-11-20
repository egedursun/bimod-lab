#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_user_roles_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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
from apps.user_permissions.models import UserRole
from apps.user_permissions.utils import PermissionNames, PredefinedRolePackages__Functional, \
    PredefinedRolePackages__Contextual
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class PermissionView_UserRoleList(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_USER_ROLES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_USER_ROLES):
            messages.error(self.request, "You do not have permission to list user roles.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        user_roles = UserRole.objects.filter(organization__in=user_orgs)
        paginator = Paginator(user_roles, 9)  # Show 9 roles per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        logger.info(f"User roles were listed by User: {self.request.user.id}.")

        # Pass the custom roles
        context['functional_roles'] = PredefinedRolePackages__Functional.get_dict()
        context['contextual_roles'] = PredefinedRolePackages__Contextual.get_dict()

        return context
