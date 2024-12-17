#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-20 14:08:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 14:08:11
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

from apps.notifications.views import (
    NotificationView_ItemListCreate,
    NotificationView_ItemDelete,
    NotificationView_MarkAllAsRead
)

app_name = 'notifications'

urlpatterns = [
    path(
        "list/",
        NotificationView_ItemListCreate.as_view(
            template_name="notifications/list_create_notification.html"
        ),
        name="list_create"
    ),

    path(
        "delete/<int:pk>/",
        NotificationView_ItemDelete.as_view(

        ),
        name="delete"
    ),

    path(
        "mark_all_as_read/",
        NotificationView_MarkAllAsRead.as_view(

        ),
        name="mark_all_as_read"
    ),
]
