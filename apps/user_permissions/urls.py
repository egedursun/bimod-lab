#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
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

from apps.user_permissions.views import AddPermissionsView, ListPermissionsView

app_name = "user_permissions"

urlpatterns = [
    path('add/', AddPermissionsView.as_view(template_name="user_permissions/add_permissions.html"),
         name="add_permissions"),
    path('list/', ListPermissionsView.as_view(template_name="user_permissions/list_permissions.html"),
         name="list_permissions"),
]
