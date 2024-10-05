#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: forum_comment_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: forum_comment_models.py
#  Last Modified: 2024-09-26 19:10:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:21:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class ForumComment(models.Model):
    """
    Represents a comment on a forum post. Comments allow users to discuss the content
    of a post and provide feedback or additional information.

    Attributes:
        id (AutoField): The primary key for the comment.
        content (TextField): The content of the comment.
        created_by (ForeignKey): The user who created the comment.
        post (ForeignKey): The post to which this comment belongs.
        created_at (DateTimeField): The date and time when the comment was created.
        updated_at (DateTimeField): The date and time when the comment was last updated.
        like_count (PositiveIntegerField): The number of unique likes this comment has received.
    """

    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    post = models.ForeignKey("ForumPost", related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)  # Storing the number of unique likes

    def __str__(self):
        return f"Comment by {self.created_by} on Post ID {self.post.id}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['content', 'created_at']),
            models.Index(fields=['content', 'created_at', 'updated_at']),
        ]
