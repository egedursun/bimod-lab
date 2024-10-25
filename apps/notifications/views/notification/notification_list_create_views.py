#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: notification_create_views.py
#  Last Modified: 2024-10-20 14:19:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 14:19:45
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.notifications.models import NotificationItem
from apps.notifications.utils import NotificationFAIconChoicesNames, NotificationTitleCategoryChoicesNames, \
    NotificationSenderTypeNames, NOTIFICATION_TITLE_CATEGORY_CHOICES
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NotificationView_ItemListCreate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        internal_notifications = NotificationItem.objects.filter(
            notification_sender_type=NotificationSenderTypeNames.SYSTEM,
            organization__in=user_orgs).order_by('-created_at')

        paginator = Paginator(internal_notifications, 10)
        page = self.request.GET.get('page')
        paginated_notifications = paginator.get_page(page)
        context['organizations'] = user_orgs
        context['internal_notifications'] = paginated_notifications
        context["notification_categories"] = NOTIFICATION_TITLE_CATEGORY_CHOICES
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_INTERNAL_NOTIFICATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_INTERNAL_NOTIFICATIONS):
            messages.error(request, "You do not have permission to create internal notifications.")
            return redirect('notifications:list_create')
        ##############################

        try:
            organization_id = request.POST.get('organization_id')
            notification_category = request.POST.get('notification_category')
            organization = Organization.objects.get(id=organization_id)
            notification_text = request.POST.get('notification_text')

            new_notification = NotificationItem.objects.create(
                organization=organization,
                notification_sender_type=NotificationSenderTypeNames.SYSTEM,
                notification_title_category=notification_category,
                notification_fa_icon=NotificationFAIconChoicesNames.BUILDING,
                notification_message=notification_text)
            new_notification.save()
            NotificationItem.add_notification_to_users(notification=new_notification, acting_user=request.user)
            logger.info(f"Notification created: {new_notification}")
            messages.success(request, 'Notification created successfully.')
            return redirect('notifications:list_create')
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            messages.error(request, 'Error creating notification.')
            return redirect('notifications:list_create')
