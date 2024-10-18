#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_topic_message_admin.py
#  Last Modified: 2024-10-17 22:18:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:18:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


"""
class HadronTopicMessage(models.Model):
    topic = models.ForeignKey('hadron_prime.HadronTopic', on_delete=models.CASCADE)
    sender_node = models.ForeignKey('hadron_prime.HadronNode', on_delete=models.CASCADE, related_name='sender_node')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic.topic_name + ' - ' + self.sender_node.node_name + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Hadron Topic Message'
        verbose_name_plural = 'Hadron Topic Messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['topic', 'sender_node']),
            models.Index(fields=['topic', 'created_at']),
        ]

"""


from django.contrib import admin

from apps.hadron_prime.models import HadronTopicMessage
from apps.hadron_prime.utils import HADRON_TOPIC_MESSAGE_ADMIN_LIST, HADRON_TOPIC_MESSAGE_ADMIN_FILTER, \
    HADRON_TOPIC_MESSAGE_ADMIN_SEARCH


@admin.register(HadronTopicMessage)
class HadronTopicMessageAdmin(admin.ModelAdmin):
    list_display = HADRON_TOPIC_MESSAGE_ADMIN_LIST
    list_filter = HADRON_TOPIC_MESSAGE_ADMIN_FILTER
    search_fields = HADRON_TOPIC_MESSAGE_ADMIN_SEARCH
    ordering = ['-created_at']
