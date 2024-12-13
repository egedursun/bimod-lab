#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: expert_network_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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


class ExpertNetwork(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='expert_networks',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=255)

    meta_description = models.TextField(default="", blank=True)

    created_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='expert_networks_created_by_user'
    )

    last_updated_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='expert_networks_updated_by_user'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expert Network"
        verbose_name_plural = "Expert Networks"
        ordering = ["-created_at"]

        unique_together = [
            [
                "organization",
                "name"
            ],
        ]

        indexes = [
            models.Index(fields=[
                "name"
            ]),
            models.Index(fields=[
                "created_by_user"
            ]),
            models.Index(fields=[
                "last_updated_by_user"
            ]),
            models.Index(fields=[
                "created_at"
            ]),
            models.Index(fields=[
                "updated_at"
            ]),
            models.Index(fields=[
                "name",
                "created_at"
            ]),
            models.Index(fields=[
                "name",
                "updated_at"
            ]),
            models.Index(fields=[
                "created_by_user",
                "created_at"
            ]),
            models.Index(fields=[
                "created_by_user",
                "updated_at"
            ]),
            models.Index(fields=[
                "last_updated_by_user",
                "created_at"
            ]),
            models.Index(fields=[
                "last_updated_by_user",
                "updated_at"
            ]),
            models.Index(fields=[
                "name",
                "created_by_user",
                "created_at"
            ]),
            models.Index(fields=[
                "name",
                "created_by_user",
                "updated_at"
            ]),
            models.Index(fields=[
                "name",
                "last_updated_by_user",
                "created_at"
            ]),
            models.Index(fields=[
                "name",
                "last_updated_by_user",
                "updated_at"
            ]),
            models.Index(fields=[
                "created_by_user",
                "created_at",
                "updated_at"
            ]),
            models.Index(fields=[
                "last_updated_by_user",
                "created_at",
                "updated_at"
            ]),
            models.Index(fields=[
                "name",
                "created_by_user",
                "created_at",
                "updated_at"
            ]),
            models.Index(fields=[
                "name",
                "last_updated_by_user",
                "created_at",
                "updated_at"
            ]),
        ]
