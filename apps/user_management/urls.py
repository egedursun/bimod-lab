#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.urls import path

from apps.user_management.views import UserManagementView_UserInvite, UserManagementView_UserList, \
    UserManagementView_UserDelete, UserManagementView_UserUpdateStatus, \
    UserManagementView_ConnectUser, UserManagementView_UserRemoveFromOrganization, UserManagementView_UserRemoveFromAll

app_name = "user_management"

urlpatterns = [
    path('add/', UserManagementView_UserInvite.as_view(template_name="user_management/users/add_new_user.html"),
         name="add"),
    path('list/', UserManagementView_UserList.as_view(template_name="user_management/users/list_users.html"),
         name="list"),
    path('remove/<int:pk>/', UserManagementView_UserDelete.as_view(
        template_name="user_management/users/confirm_remove_user.html"), name="remove"),
    path('update_user_status/', UserManagementView_UserUpdateStatus.as_view(), name='update_user_status'),
    path('add_user_to_organization/', UserManagementView_ConnectUser.as_view(
        template_name="user_management/connections/add_user_to_organization.html"), name='add_user_to_organization'),
    path('remove_user_from_organization/<int:pk>/<int:org_id>/', UserManagementView_UserRemoveFromOrganization.as_view(
        template_name="user_management/connections/confirm_remove_from_organization.html"),
         name='remove_user_from_organization'),
    path('remove_user_from_all_organizations/<int:pk>/', UserManagementView_UserRemoveFromAll.as_view(
        template_name="user_management/connections/confirm_remove_from_all_organizations.html"),
         name='remove_user_from_all_organizations'),
]
