#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_system_models.py
#  Last Modified: 2024-10-17 21:47:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 21:47:41
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


class HadronSystem(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )

    system_name = models.CharField(max_length=4000, unique=True)

    system_description = models.TextField()

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.system_name + ' - ' + self.organization.name

    class Meta:
        verbose_name = 'Hadron System'
        verbose_name_plural = 'Hadron Systems'

        ordering = ['-created_at']

        unique_together = [
            [
                'organization',
                'system_name'
            ],
        ]

        indexes = [
            models.Index(fields=[
                'organization',
                'system_name'
            ]),
            models.Index(fields=[
                'organization',
                'created_by_user'
            ]),
            models.Index(fields=[
                'organization',
                'created_at'
            ]),
            models.Index(fields=[
                'organization',
                'updated_at'
            ]),
        ]
