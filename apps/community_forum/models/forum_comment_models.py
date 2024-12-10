#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: forum_comment_models.py
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


class ForumComment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        "ForumPost",
        related_name='comments',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.created_by} on Post ID {self.post.id}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=[
                    'content',
                    'created_at'
                ]
            ),
            models.Index(
                fields=[
                    'content',
                    'created_at',
                    'updated_at'
                ]
            ),
        ]
