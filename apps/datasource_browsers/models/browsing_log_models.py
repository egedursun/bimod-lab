#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: browsing_log_models.py
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

from apps.datasource_browsers.models.browser_connection_models import (
    DataSourceBrowserConnection
)


class DataSourceBrowserBrowsingLog(models.Model):
    connection = models.ForeignKey(
        DataSourceBrowserConnection,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    action = models.CharField(max_length=1000)

    context_url = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )

    html_content = models.TextField(blank=True, null=True)
    context_content = models.TextField(blank=True, null=True)
    log_content = models.TextField(blank=True, null=True)

    screenshot = models.ImageField(
        upload_to="datasource_browser_screenshots/%Y/%m/%d",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.connection.name + " - " + self.action + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Data Source Browser Browsing Log"
        verbose_name_plural = "Data Source Browser Browsing Logs"

        indexes = [
            models.Index(
                fields=[
                    "connection",
                    "action",
                    "created_at",
                ]
            ),
            models.Index(
                fields=[
                    "connection",
                    "action",
                    "created_at",
                    "context_url",
                ]
            ),
            models.Index(
                fields=[
                    "connection",
                    "action",
                    "created_at",
                    "context_url",
                    "html_content",
                ]
            ),
            models.Index(
                fields=[
                    "connection",
                    "action",
                    "created_at",
                    "context_url",
                    "html_content",
                    "context_content",
                ]
            ),
        ]
