#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: browser_connection_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from apps.datasource_browsers.utils import (
    BROWSER_TYPES
)


class DataSourceBrowserConnection(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)

    browser_type = models.CharField(
        max_length=100,
        choices=BROWSER_TYPES
    )

    assistant = models.ForeignKey(
        "assistants.Assistant",
        on_delete=models.CASCADE
    )

    data_selectivity = models.FloatField(default=0.5)

    whitelisted_extensions = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    blacklisted_extensions = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    reading_abilities = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    minimum_investigation_sites = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.browser_type + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        unique_together = [
            ["assistant", "name"],
        ]

        verbose_name = "Data Source Browser Connection"
        verbose_name_plural = "Data Source Browser Connections"

        indexes = [
            models.Index(
                fields=[
                    "assistant",
                    "name",
                    "browser_type",
                    "created_at",
                ]
            ),
            models.Index(
                fields=[
                    "assistant",
                    "name",
                    "browser_type",
                    "created_at",
                    "updated_at",
                ]
            ),
            models.Index(
                fields=[
                    "assistant",
                    "name",
                    "browser_type",
                    "created_at",
                    "created_by_user",
                ]
            ),
        ]
