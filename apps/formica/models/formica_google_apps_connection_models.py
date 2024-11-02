#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: formica_google_apps_connection_models.py
#  Last Modified: 2024-11-02 12:46:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 12:46:49
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


class FormicaGoogleAppsConnection(models.Model):
    formica_assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, null=True, blank=True)
    owner_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    connection_api_key = models.CharField(max_length=4000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.formica_assistant.name + ' - ' + self.owner_user.username + ' - ' + self.connection_api_key

    class Meta:
        verbose_name = 'Formica Google Apps Connection'
        verbose_name_plural = 'Formica Google Apps Connections'
        indexes = [
            models.Index(fields=['formica_assistant']),
            models.Index(fields=['owner_user']),
            models.Index(fields=['formica_assistant', 'owner_user']),
        ]
        unique_together = [
            ['formica_assistant', 'owner_user'],
        ]
