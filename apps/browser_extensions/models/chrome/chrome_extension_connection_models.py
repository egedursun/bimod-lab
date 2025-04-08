#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chrome_extension_connection_models.py
#  Last Modified: 2024-12-23 09:37:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-23 09:37:01
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


class ChromeExtensionConnection(models.Model):
    chrome_assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    owner_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    connection_api_key = models.CharField(
        max_length=4000
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.chrome_assistant.name + ' - ' + self.owner_user.username + ' - ' + self.connection_api_key

    class Meta:
        verbose_name = 'Google Chrome Extension Connection'
        verbose_name_plural = 'Google Chrome Extension Connections'

        indexes = [
            models.Index(fields=[
                'chrome_assistant'
            ]),
            models.Index(fields=[
                'owner_user'
            ]),
            models.Index(fields=[
                'chrome_assistant',
                'owner_user'
            ]),
        ]

        unique_together = [
            [
                'chrome_assistant',
                'owner_user'
            ],
        ]

