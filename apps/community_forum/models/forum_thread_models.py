#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: forum_thread_models.py
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
#
#
#

from django.db import models


class ForumThread(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey("ForumCategory", related_name='threads', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Forum Thread"
        verbose_name_plural = "Forum Threads"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['title', 'created_at']),
            models.Index(fields=['title', 'created_at', 'updated_at']),
        ]
