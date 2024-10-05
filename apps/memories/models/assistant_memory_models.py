#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: assistant_memory_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.db import models

from apps.memories.utils import MEMORY_TYPE


class AssistantMemory(models.Model):
    """
    AssistantMemory Model:
    - Purpose: Represents a memory associated with a specific user and assistant, storing content that can be either user-specific or assistant-specific.
    - Key Fields:
        - `user`: ForeignKey linking to the `User` model, representing the user associated with the memory.
        - `assistant`: ForeignKey linking to the `Assistant` model, representing the assistant associated with the memory.
        - `memory_type`: The type of memory, indicating whether it's user-specific or assistant-specific.
        - `memory_text_content`: The textual content of the memory.
        - `created_at`: Timestamp for when the memory was created.
    - Meta:
        - `verbose_name`: "Memory"
        - `verbose_name_plural`: "Memories"
        - `ordering`: Orders memories by creation date in descending order.
        - `indexes`: Indexes on various fields, including combinations of `assistant`, `user`, and `created_at` for optimized queries.
    """

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    memory_type = models.CharField(max_length=50, choices=MEMORY_TYPE, default="user-specific")
    memory_text_content = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assistant} - {self.memory_type}"

    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["assistant", "user", "created_at"]),
            models.Index(fields=["assistant", "user"]),
            models.Index(fields=["assistant", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]
