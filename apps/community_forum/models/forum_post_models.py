#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: forum_post_models.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.db import models


class ForumPost(models.Model):
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
