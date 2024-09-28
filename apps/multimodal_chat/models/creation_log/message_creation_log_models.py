#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.


from django.db import models


# NOTE: Counts both the Normal Chat Messages and Lean Chat Messages
class ChatMessageCreationLog(models.Model):
    """
    ChatMessageCreationLog Model:
    - Purpose: Represents a log entry for the creation of a message within a multimodal chat. It stores the organization associated with the message and the timestamp of creation.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` model.
        - `created_at`: Timestamp for when the message was created.
    - Meta:
        - `verbose_name`: "Chat Message Creation Log"
        - `verbose_name_plural`: "Chat Message Creation Logs"
        - `ordering`: Orders logs by creation date in descending order.
        - `indexes`: Indexes on the creation date for optimized queries.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = "Chat Message Creation Log"
        verbose_name_plural = "Chat Message Creation Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['created_at']),
        ]
