#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_folder_models.py
#  Last Modified: 2024-10-14 18:32:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:32:44
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


class DraftingFolder(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    meta_context_instructions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.organization.name + ' - ' + self.name

    class Meta:
        verbose_name = 'Drafting Folder'
        verbose_name_plural = 'Drafting Folders'

        indexes = [
            models.Index(fields=[
                'organization'
            ]),
            models.Index(fields=[
                'organization',
                'name'
            ]),
        ]

        unique_together = [
            [
                'organization',
                'name'
            ],
        ]
