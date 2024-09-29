#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: browser_connection_models.py
#  Last Modified: 2024-09-26 20:04:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:31:49
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models

from apps.datasource_browsers.utils import BROWSER_TYPES


class DataSourceBrowserConnection(models.Model):
    """
    DataSourceBrowserConnection Model:
    - Purpose: Represents a browser connection used as a data source, with configurations for selectivity, allowed and disallowed extensions, and reading abilities.
    - Key Fields:
        - `name`: The name of the browser connection.
        - `description`: A brief description of the connection.
        - `browser_type`: The type of browser being used (e.g., Google).
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `data_selectivity`: Float field representing the selectivity of data scraping.
        - `whitelisted_extensions`: JSONField for storing allowed file extensions.
        - `blacklisted_extensions`: JSONField for storing disallowed file extensions.
        - `reading_abilities`: JSONField for defining the browser's reading abilities.
        - `minimum_investigation_sites`: Minimum number of sites to investigate.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the user who created the connection.
    """

    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    browser_type = models.CharField(max_length=100, choices=BROWSER_TYPES)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)

    # hyper-parameters
    data_selectivity = models.FloatField(default=0.5)
    whitelisted_extensions = models.JSONField(default=list, blank=True, null=True)
    blacklisted_extensions = models.JSONField(default=list, blank=True, null=True)
    reading_abilities = models.JSONField(default=list, blank=True, null=True)
    minimum_investigation_sites = models.IntegerField(default=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.browser_type + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Data Source Browser Connection"
        verbose_name_plural = "Data Source Browser Connections"
