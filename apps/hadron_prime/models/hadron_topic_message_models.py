#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_topic_message_models.py
#  Last Modified: 2024-10-17 21:47:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 21:48:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.db import models


class HadronTopicMessage(models.Model):
    topic = models.ForeignKey(
        'hadron_prime.HadronTopic',
        on_delete=models.CASCADE
    )

    sender_node = models.ForeignKey(
        'hadron_prime.HadronNode',
        on_delete=models.CASCADE,
        related_name='sender_node'
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic.topic_name + ' - ' + self.sender_node.node_name + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Hadron Topic Message'
        verbose_name_plural = 'Hadron Topic Messages'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'topic',
                'sender_node'
            ]),
            models.Index(fields=[
                'topic',
                'created_at'
            ]),
        ]
