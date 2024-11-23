#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_030_user_roles_create.py
#  Last Modified: 2024-11-19 05:09:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-19 05:09:34
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

from django.contrib.auth.models import User

from apps.quick_setup_helper.utils import UserRoleQuickIntegrationChoicesNames
from apps.user_permissions.models import UserRole, UserPermission
from apps.user_permissions.utils import PredefinedRolePackages__Functional, PredefinedRolePackages__Contextual

logger = logging.getLogger(__name__)


def action__030_user_roles_create(
    metadata__user,
    metadata__organization,
    metadata__invited_new_users,
    response__user_roles_option
):
    try:

        # Grant users full access rights within the application (admin package - except permission management rights -).
        if response__user_roles_option == UserRoleQuickIntegrationChoicesNames.FULL_ACCESS:
            selected_roles = [
                PredefinedRolePackages__Contextual.Names.OrganizationAdmin,
                PredefinedRolePackages__Contextual.Names.FinanceAdmin,
                PredefinedRolePackages__Functional.Names.CreationAdminRole,
                PredefinedRolePackages__Functional.Names.ModificationAdminRole,
                PredefinedRolePackages__Functional.Names.ReadAdminRole,
                PredefinedRolePackages__Functional.Names.DeletionAdminRole,
            ]

        # Grant users moderator rights within the application (CRUD right - ( except organization, llm, balance, etc. related rights -).
        elif response__user_roles_option == UserRoleQuickIntegrationChoicesNames.MODERATION_ACCESS:
            selected_roles = [
                PredefinedRolePackages__Functional.Names.CreationAdminRole,
                PredefinedRolePackages__Functional.Names.ModificationAdminRole,
                PredefinedRolePackages__Functional.Names.ReadAdminRole,
                PredefinedRolePackages__Functional.Names.DeletionAdminRole,
            ]

        # Grant users only with the interaction rights (Chat / Communication etc. related rights only).
        elif response__user_roles_option == UserRoleQuickIntegrationChoicesNames.LIMITED_ACCESS:
            selected_roles = [
                PredefinedRolePackages__Functional.Names.ReadAdminRole,
                PredefinedRolePackages__Contextual.Names.ChatInteractionUser,
                PredefinedRolePackages__Contextual.Names.ScriptingUser,
                PredefinedRolePackages__Contextual.Names.DeveloperUser,
                PredefinedRolePackages__Contextual.Names.SupportUser,
                PredefinedRolePackages__Contextual.Names.OfficeUser,
            ]

        else:
            logger.error(f"Invalid user roles option: {response__user_roles_option}")
            return False

        new_user_roles = []
        for selected_rol_name in selected_roles:
            # Create the relevant user role(s)
            boilerplate_role_description = f"Boilerplate role definition for {metadata__organization.name} with authorization code {selected_rol_name}."

            role_permissions = get_boilerplate_role_permissions(boilerplate_role_name=selected_rol_name)

            structured_permission_list = []
            for permission_db_code, permission_label in role_permissions:
                structured_permission_list.append(permission_db_code)

            new_user_role = UserRole.objects.create(
                organization=metadata__organization,
                role_name=selected_rol_name,
                role_description=boilerplate_role_description,
                role_permissions=structured_permission_list,
                created_by_user=metadata__user
            )
            new_user_roles.append(new_user_role)

        # Add the user role to the invited users
        for invited_new_user in metadata__invited_new_users:
            user: User
            try:

                for new_user_role in new_user_roles:
                    new_user_role: UserRole

                    # Add the permissions of the role to the users
                    success_add_permissions = update_user_permissions(user=invited_new_user, role=new_user_role)

                    if success_add_permissions is True:

                        # Add the user to the UserRole's users
                        new_user_role.users.add(invited_new_user)
                        new_user_role.save()

                    else:

                        logger.error(f"Failed to add permissions to user with email address {invited_new_user.email}")
                        continue

            except Exception as e:
                logger.error(f"Failed to assign role to user with email address {invited_new_user.email}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__030_user_roles_create: {str(e)}")

    logger.info("Action action__030_user_roles_create completed successfully.")
    return True


def get_boilerplate_role_permissions(boilerplate_role_name: str):
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
    ### Contextual .
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
    else:
        return []

    return boilerplate_role_permissions


def update_user_permissions(user: User, role: UserRole):
    try:
        for perm_code in role.role_permissions:
            try:
                user_permission, created = UserPermission.objects.get_or_create(
                    user=user,
                    permission_type=perm_code
                )
            except Exception as e:
                logger.error(f"Error adding permission '{perm_code}' for user {user.username}")
                continue

    except Exception as e:
        logger.error(f"Error updating user permissions: {str(e)}")
        return False

    logger.info(f"User permissions updated for User: {user.id}.")
    return True
