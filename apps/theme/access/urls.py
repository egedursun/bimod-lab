#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path
from .views import AccessView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/access/roles/",
        login_required(AccessView.as_view(template_name="app_access_roles.html")),
        name="app-access-roles",
    ),
    path(
        "app/access/permission/",
        login_required(AccessView.as_view(template_name="app_access_permission.html")),
        name="app-access-permission",
    ),
]
