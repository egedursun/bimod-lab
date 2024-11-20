#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_boilerplate_role_views.py
#  Last Modified: 2024-11-19 04:37:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-19 04:37:38
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

from apps.organization.models import Organization
from apps.user_permissions.models import UserRole
from apps.user_permissions.utils import PredefinedRolePackages__Functional, PredefinedRolePackages__Contextual

logger = logging.getLogger(__name__)


class PermissionView_IntegrateBoilerplateRole(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        try:
            user_orgs = Organization.objects.filter(users__in=[request.user])
            boilerplate_role_name = request.POST.get('boilerplate_role_name')
            boilerplate_role_created_by_user = request.user

            boilerplate_role_permissions = []
            ###
            ### Functional
            ###
            if boilerplate_role_name == PredefinedRolePackages__Functional.Names.SuperUserAdminRole:
                boilerplate_role_permissions = PredefinedRolePackages__Functional.SuperUserAdminRole.get()
            elif boilerplate_role_name == PredefinedRolePackages__Functional.Names.CreationAdminRole:
                boilerplate_role_permissions = PredefinedRolePackages__Functional.CreationAdminRole.get()
            elif boilerplate_role_name == PredefinedRolePackages__Functional.Names.ModificationAdminRole:
                boilerplate_role_permissions = PredefinedRolePackages__Functional.ModificationAdminRole.get()
            elif boilerplate_role_name == PredefinedRolePackages__Functional.Names.ReadAdminRole:
                boilerplate_role_permissions = PredefinedRolePackages__Functional.ReadAdminRole.get()
            elif boilerplate_role_name == PredefinedRolePackages__Functional.Names.DeletionAdminRole:
                boilerplate_role_permissions = PredefinedRolePackages__Functional.DeletionAdminRole.get()
            ###
            ### Contextual
            ###
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.PermissionAdmin__Dangerous:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.PermissionAdmin__Dangerous.get(),
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.OrganizationAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.OrganizationAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.AssistantAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.AssistantAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.UsersAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.UsersAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.FinanceAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.FinanceAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.ChatInteractionUser:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.ChatInteractionUser.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.NotificationAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.NotificationAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.DataSourceAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.DataSourceAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.SecurityAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.SecurityAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.SupportUser:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.SupportUser.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.ScriptingUser:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.ScriptingUser.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.DeveloperUser:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.DeveloperUser.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.BlockchainAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.BlockchainAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.HardwareAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.HardwareAdmin.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.OfficeUser:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.OfficeUser.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.PromptEngineerUser:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.PromptEngineerUser.get()
            elif boilerplate_role_name == PredefinedRolePackages__Contextual.Names.ProjectTeamAdmin:
                boilerplate_role_permissions = PredefinedRolePackages__Contextual.ProjectTeamAdmin.get()

            if boilerplate_role_permissions is []:
                messages.error(request, "Error integrating boilerplate role.")
                return redirect('user_permissions:list_user_roles')

            structured_permission_list = []
            for permission_db_code, permission_label in boilerplate_role_permissions:
                structured_permission_list.append(permission_db_code)

            for user_org in user_orgs:
                user_org: Organization

                boilerplate_role_description = f"Boilerplate role definition for {user_org.name} with authorization code {boilerplate_role_name}."

                UserRole.objects.create(
                    organization=user_org,
                    role_name=boilerplate_role_name,
                    role_description=boilerplate_role_description,
                    role_permissions=structured_permission_list,
                    created_by_user=boilerplate_role_created_by_user
                )

            messages.success(request, f"Boilerplate role '{boilerplate_role_name}' integrated successfully.")
            return redirect('user_permissions:list_user_roles')

        except Exception as e:
            logger.error(f"Error integrating boilerplate role: {e}")
            messages.error(request, "Error integrating boilerplate role.")
            return redirect('user_permissions:list_user_roles')
