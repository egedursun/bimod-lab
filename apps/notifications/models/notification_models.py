#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: notification_models.py
#  Last Modified: 2024-10-20 14:08:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 14:08:29
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

from django.contrib.auth.models import User
from django.db import models

from apps.notifications.utils import (NOTIFICATION_FA_ICON_CHOICES, NOTIFICATION_TITLE_CATEGORY_CHOICES,
                                      NOTIFICATION_SENDER_TYPES, NotificationSenderTypeNames)
from apps.organization.models import Organization

logger = logging.getLogger(__name__)


class OrderedNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')


class NotificationItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='associated_notifications', null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.CASCADE)
    notification_sender_type = models.CharField(max_length=1000, choices=NOTIFICATION_SENDER_TYPES,
                                                default=NotificationSenderTypeNames.BIMOD_TEAM)
    notification_title_category = models.CharField(max_length=1000, choices=NOTIFICATION_TITLE_CATEGORY_CHOICES,
                                                   default='info')
    notification_fa_icon = models.CharField(max_length=1000, choices=NOTIFICATION_FA_ICON_CHOICES,
                                            default='fa fa-bell')

    notification_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    readers = models.ManyToManyField('auth.User', related_name='read_notifications', blank=True)
    objects = OrderedNotificationManager()

    def __str__(self):
        return self.notification_title_category + ' - ' + str(self.created_at)

    class Meta:
        verbose_name = 'Notification Item'
        verbose_name_plural = 'Notification Items'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['notification_sender_type', 'created_at']),
            models.Index(fields=['notification_title_category', 'created_at']),
            models.Index(fields=['notification_fa_icon', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    @staticmethod
    def add_notification_to_user(notification, user):
        try:
            if notification not in user.profile.notifications.all():
                user.profile.notifications.add(notification)
                logger.info(f"Notification added to user: {user}")
            else:
                logger.info("Notification already added to user, skipping...")
        except Exception as e:
            logger.error(f"Error adding notification to user: {e}")

    @staticmethod
    def add_notification_to_users(notification, acting_user):
        orgs_users = []
        if notification.notification_sender_type == NotificationSenderTypeNames.SYSTEM:
            user_orgs = Organization.objects.filter(users__in=[acting_user])
            for org in user_orgs:
                orgs_users += org.users.all()
            orgs_users = list(set(orgs_users))
        elif notification.notification_sender_type == NotificationSenderTypeNames.BIMOD_TEAM:
            orgs_users = User.objects.all()  # Send to all users

        for user in orgs_users:
            try:
                if notification not in user.profile.notifications.all():
                    user.profile.notifications.add(notification)
                    logger.info(f"Notification added to user: {user}")
                else:
                    logger.info("Notification already added to user, skipping...")
            except Exception as e:
                logger.error(f"Error adding notification to user: {e}")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.notification_sender_type == NotificationSenderTypeNames.BIMOD_TEAM:
            self.add_notification_to_users(notification=self, acting_user=None)
        elif self.notification_sender_type == NotificationSenderTypeNames.WELCOME:
            self.add_notification_to_user(notification=self, user=self.user)
