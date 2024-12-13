#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_topic_models.py
#  Last Modified: 2024-10-17 21:47:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 21:48:35
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


from apps.hadron_prime.utils import (
    HADRON_TOPIC_CATEGORIES
)


class HadronTopic(models.Model):
    system = models.ForeignKey(
        'HadronSystem',
        on_delete=models.CASCADE
    )

    topic_name = models.CharField(max_length=4000)
    topic_description = models.TextField()
    topic_purpose = models.TextField()

    topic_category = models.CharField(
        max_length=100,
        choices=HADRON_TOPIC_CATEGORIES
    )

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic_name + ' - ' + self.system.system_name + ' - ' + self.system.organization.name

    class Meta:
        verbose_name = 'Hadron Topic'
        verbose_name_plural = 'Hadron Topics'

        ordering = ['-created_at']

        unique_together = [
            [
                "system",
                "topic_name"
            ],
        ]

        indexes = [
            models.Index(fields=[
                'system',
                'topic_name'
            ]),
            models.Index(fields=[
                'system',
                'created_by_user'
            ]),
            models.Index(fields=[
                'system',
                'created_at'
            ]),
            models.Index(fields=[
                'system',
                'updated_at'
            ]),
        ]
