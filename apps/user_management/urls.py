#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-02 12:34:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:10:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.user_management.views import AddNewUserView, ListUsersView, RemoveUserView, UpdateUserStatusView, \
    AddUserToOrganizationView, RemoveUserFromOrganizationView, RemoveUserFromAllOrganizationsView

app_name = "user_management"

urlpatterns = [
    path('add/', AddNewUserView.as_view(template_name="user_management/users/add_new_user.html"), name="add"),
    path('list/', ListUsersView.as_view(template_name="user_management/users/list_users.html"), name="list"),
    path('remove/<int:pk>/', RemoveUserView.as_view(template_name="user_management/users/confirm_remove_user.html"),
         name="remove"),
    path('update_user_status/', UpdateUserStatusView.as_view(), name='update_user_status'),

    path('add_user_to_organization/', AddUserToOrganizationView.as_view(
        template_name="user_management/connections/add_user_to_organization.html"),
         name='add_user_to_organization'),
    path('remove_user_from_organization/<int:pk>/<int:org_id>/', RemoveUserFromOrganizationView.as_view(
        template_name="user_management/connections/confirm_remove_from_organization.html"
    ), name='remove_user_from_organization'),

    path('remove_user_from_all_organizations/<int:pk>/', RemoveUserFromAllOrganizationsView.as_view(
        template_name="user_management/connections/confirm_remove_from_all_organizations.html"
    ), name='remove_user_from_all_organizations'),
]
