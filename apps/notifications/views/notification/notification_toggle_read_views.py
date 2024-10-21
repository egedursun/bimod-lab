#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: notification_toggle_read_views.py
#  Last Modified: 2024-10-20 16:59:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 16:59:15
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.notifications.models import NotificationItem

logger = logging.getLogger(__name__)


class NotificationView_MarkAllAsRead(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            user_notifications = user.profile.notifications.all()
            for notification in user_notifications:
                notification: NotificationItem
                notification.readers.add(user) if notification.readers is not None else notification.readers.set(
                    [user])
                notification.save()
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return redirect("notifications:list_create")

        logger.info(f"All notifications marked as read for user.")
        return redirect("notifications:list_create")
