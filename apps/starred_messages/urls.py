#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-02 12:34:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:08:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.starred_messages.views import ListStarredMessageView, DeleteStarredMessageView

app_name = "starred_messages"

urlpatterns = [
    path("list/", ListStarredMessageView.as_view(
        template_name="starred_messages/list_starred_messages.html"
    ), name="list"),
    path("delete/<int:pk>/", DeleteStarredMessageView.as_view(), name="delete"),
]
