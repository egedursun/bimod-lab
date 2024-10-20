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
                                      NotificationTitleCategoryChoicesNames)


logger = logging.getLogger(__name__)


class OrderedNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')


class NotificationItem(models.Model):
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='notifications')
    notification_fa_icon = models.CharField(max_length=1000, choices=NOTIFICATION_FA_ICON_CHOICES,
                                            default='fa fa-bell')
    notification_fa_icon_color = models.CharField(max_length=1000, default='btn-primary', blank=True)
    notification_title_category = models.CharField(max_length=1000, choices=NOTIFICATION_TITLE_CATEGORY_CHOICES,
                                                   default='info')
    notification_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    readers = models.ManyToManyField('auth.User', related_name='read_notifications', blank=True)

    # Custom Manager to enforce ordering.
    objects = OrderedNotificationManager()

    bimod_admin_notification = models.BooleanField(default=False)

    def __str__(self):
        return self.notification_title_category + ' - ' + self.user.username + ' - ' + str(self.created_at)

    class Meta:
        verbose_name = 'Notification Item'
        verbose_name_plural = 'Notification Items'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        if self.notification_fa_icon_color == '':
            if self.notification_title_category == NotificationTitleCategoryChoicesNames.HumanReadable.BIMOD_TEAM:
                self.notification_fa_icon_color = 'btn-primary'
            elif self.notification_title_category == NotificationTitleCategoryChoicesNames.HumanReadable.INTERNAL:
                self.notification_fa_icon_color = 'btn-primary'
            elif self.notification_title_category == NotificationTitleCategoryChoicesNames.HumanReadable.INFO:
                self.notification_fa_icon_color = 'btn-info'
            elif self.notification_title_category == NotificationTitleCategoryChoicesNames.HumanReadable.WARNING:
                self.notification_fa_icon_color = 'btn-warning'
            elif self.notification_title_category == NotificationTitleCategoryChoicesNames.HumanReadable.ERROR:
                self.notification_fa_icon_color = 'btn-danger'
            elif self.notification_title_category == NotificationTitleCategoryChoicesNames.HumanReadable.ALERT:
                self.notification_fa_icon_color = 'btn-danger'
            else:
                self.notification_fa_icon_color = 'btn-dark'

        if self.bimod_admin_notification is True and self.notification_title_category == NotificationTitleCategoryChoicesNames.BIMOD_TEAM:
            self.organization = None
            all_users = User.objects.all()
            for user in all_users:
                try:
                    if self not in user.notifications.all():
                        user.notifications.add(self)
                except Exception as e:
                    logger.error(f"Error adding notification to user: {e}")
            logger.info(f"Notification created for all users.")
        super(NotificationItem, self).save(*args, **kwargs)

