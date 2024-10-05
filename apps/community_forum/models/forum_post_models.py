#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: forum_post_models.py
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
#  File: forum_post_models.py
#  Last Modified: 2024-09-26 19:10:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:21:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class ForumPost(models.Model):
    """
    Represents a post within a forum thread. Posts contain the content contributed
    by users in response to the thread's topic.

    Attributes:
        id (AutoField): The primary key for the post.
        thread (ForeignKey): The thread to which this post belongs.
        content (TextField): The content of the post.
        created_by (ForeignKey): The user who created the post.
        created_at (DateTimeField): The date and time when the post was created.
        updated_at (DateTimeField): The date and time when the post was last updated.
        is_verified (BooleanField): A flag indicating whether the post contains a verified answer.
        verified_comment (OneToOneField): The comment that is marked as the verified answer for this post.
    """

    id = models.AutoField(primary_key=True)
    thread = models.ForeignKey("ForumThread", related_name='posts', on_delete=models.CASCADE)

    content = models.TextField()
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)  # Verification status for an answer
    verified_comment = models.OneToOneField("ForumComment", related_name='verified_post', on_delete=models.CASCADE,
                                            null=True, blank=True)

    def verify_comment(self, comment):
        """
        Marks the given comment as the verified comment for this post.

        Args:
            comment (ForumComment): The comment to be verified.
        """
        if self.created_by == comment.created_by:
            self.verified_comment = comment
            self.is_verified = True
            self.save()

    def __str__(self):
        return f"Post by {self.created_by} in {self.thread.title}"

    class Meta:
        verbose_name = "Forum Post"
        verbose_name_plural = "Forum Posts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['content', 'created_at']),
            models.Index(fields=['content', 'created_at', 'updated_at']),
        ]
