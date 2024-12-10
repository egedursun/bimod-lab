#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: forum_like_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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


class ForumLike(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    comment = models.ForeignKey(
        "ForumComment",
        related_name='likes',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user} on Comment ID {self.comment.id}"

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

        ordering = ["-created_at"]

        unique_together = [
            [
                'user',
                'comment'
            ],
        ]

        indexes = [
            models.Index(
                fields=[
                    'user',
                    'comment',
                    'created_at'
                ]
            ),
        ]
