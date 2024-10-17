#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
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
#
#
#

from django.urls import path

from apps.user_permissions.views import PermissionView_PermissionCreate, PermissionView_PermissionList, \
    PermissionView_UserRoleManage, \
    PermissionView_UserRoleList, PermissionView_UserRoleCreate, PermissionView_UserRoleUpdate, \
    PermissionView_UserRoleDelete

app_name = "user_permissions"

urlpatterns = [
    path('add/', PermissionView_PermissionCreate.as_view(
        template_name="user_permissions/permissions/add_permissions.html"), name="add_permissions"),
    path('list/', PermissionView_PermissionList.as_view(
        template_name="user_permissions/permissions/list_permissions.html"), name="list_permissions"),
    path('roles/add/', PermissionView_UserRoleCreate.as_view(
        template_name="user_permissions/roles/add_user_role.html"), name="add_user_role"),
    path('roles/list/', PermissionView_UserRoleList.as_view(
        template_name="user_permissions/roles/list_user_roles.html"), name="list_user_roles"),
    path('roles/manage/', PermissionView_UserRoleManage.as_view(
        template_name="user_permissions/roles/manage_user_roles.html"), name="manage_user_roles"),
    path('roles/delete/<int:pk>/', PermissionView_UserRoleDelete.as_view(
        template_name="user_permissions/roles/confirm_delete_user_role.html"), name="delete_user_role"),
    path('roles/update/<int:pk>/', PermissionView_UserRoleUpdate.as_view(
        template_name="user_permissions/roles/update_user_role.html"), name="update_user_role"),
]
