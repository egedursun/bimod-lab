#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: semantor_configuration_models.py
#  Last Modified: 2024-11-10 00:33:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 00:33:35
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


class SemantorConfiguration(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    is_local_network_active = models.BooleanField(default=True)
    is_global_network_active = models.BooleanField(default=True)

    maximum_assistant_search_items = models.IntegerField(default=5)
    maximum_integration_search_items = models.IntegerField(default=5)

    temporary_data_source_and_tool_access = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Semantor Configuration'
        verbose_name_plural = 'Semantor Configurations'
        indexes = [
            models.Index(fields=['user', 'is_local_network_active', 'is_global_network_active']),
            models.Index(fields=['user', 'is_local_network_active', 'is_global_network_active',
                                 'maximum_assistant_search_items']),
            models.Index(fields=['user', 'is_local_network_active', 'is_global_network_active',
                                 'maximum_integration_search_items']),
            models.Index(fields=['user', 'is_local_network_active', 'is_global_network_active',
                                 'maximum_assistant_search_items', 'maximum_integration_search_items']),
        ]

    def __str__(self):
        return self.user.username + ' - ' + str(self.id) + ' - ' + str(self.is_local_network_active) + ' - ' + str(
            self.is_global_network_active)
