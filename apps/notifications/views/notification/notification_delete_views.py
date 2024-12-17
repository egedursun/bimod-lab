#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: notification_delete_views.py
#  Last Modified: 2024-10-20 14:19:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 14:19:57
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

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.notifications.models import (
    NotificationItem
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class NotificationView_ItemDelete(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_INTERNAL_NOTIFICATIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_INTERNAL_NOTIFICATIONS
        ):
            messages.error(request, "You do not have permission to delete internal notifications.")

            return redirect('notifications:list_create')
        ##############################

        try:
            notification_id = kwargs.get('pk')

            notification = get_object_or_404(
                NotificationItem,
                id=notification_id
            )

            notification.delete()

            logger.info(f"Notification deleted: {notification_id} by {request.user.username}")
            messages.success(request, 'Notification deleted successfully.')

        except NotificationItem.DoesNotExist:
            logger.error(f"Notification not found.")
            messages.error(request, 'Notification not found.')

        except Exception as e:
            logger.error(f"Error deleting notification: {e}")
            messages.error(request, 'An error occurred while trying to delete the notification.')

        return redirect('notifications:list_create')
