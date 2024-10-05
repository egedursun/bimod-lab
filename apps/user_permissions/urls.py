#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-29 19:58:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-02 12:34:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:10:51
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.user_permissions.views import AddPermissionsView, ListPermissionsView, ManageUserRolesView, \
    ListUserRolesView, AddUserRoleView, UpdateUserRoleView, DeleteUserRoleView

app_name = "user_permissions"

urlpatterns = [
    path('add/', AddPermissionsView.as_view(template_name="user_permissions/permissions/add_permissions.html"),
         name="add_permissions"),
    path('list/', ListPermissionsView.as_view(template_name="user_permissions/permissions/list_permissions.html"),
         name="list_permissions"),
    #####
    path('roles/add/', AddUserRoleView.as_view(template_name="user_permissions/roles/add_user_role.html"),
            name="add_user_role"),
    path('roles/list/', ListUserRolesView.as_view(template_name="user_permissions/roles/list_user_roles.html"),
            name="list_user_roles"),
    path('roles/manage/', ManageUserRolesView.as_view(template_name="user_permissions/roles/manage_user_roles.html"),
            name="manage_user_roles"),
    path('roles/delete/<int:pk>/', DeleteUserRoleView.as_view(template_name="user_permissions/roles/confirm_delete_user_role.html"),
            name="delete_user_role"),
    path('roles/update/<int:pk>/', UpdateUserRoleView.as_view(template_name="user_permissions/roles/update_user_role.html"),
            name="update_user_role"),
]
