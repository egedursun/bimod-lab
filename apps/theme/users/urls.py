#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-06-28 19:08:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

from django.urls import path
from .views import UsersView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/user/list/",
        login_required(UsersView.as_view(template_name="app_user_list.html")),
        name="app-user-list",
    ),
    path(
        "app/user/view/account/",
        login_required(UsersView.as_view(template_name="app_user_view_account.html")),
        name="app-user-view-account",
    ),
    path(
        "app/user/view/security/",
        login_required(UsersView.as_view(template_name="app_user_view_security.html")),
        name="app-user-view-security",
    ),
    path(
        "app/user/view/billing/",
        login_required(UsersView.as_view(template_name="app_user_view_billing.html")),
        name="app-user-view-billing",
    ),
    path(
        "app/user/view/notifications/",
        login_required(UsersView.as_view(template_name="app_user_view_notifications.html")),
        name="app-user-view-notifications",
    ),
    path(
        "app/user/view/connections/",
        login_required(UsersView.as_view(template_name="app_user_view_connections.html")),
        name="app-user-view-connections",
    ),
]
