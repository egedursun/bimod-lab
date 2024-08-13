"""
Module Overview: This module defines the `MessageTemplate` model, which represents message templates created by users within an organization. The model stores the template text, metadata about its creation and update, and links to the associated user and organization.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
"""

from django.db import models


class MessageTemplate(models.Model):
    """
    MessageTemplate Model:
    - Purpose: Represents a message template associated with a specific user and organization, storing the template text and metadata about its creation and last update.
    - Key Fields:
        - `user`: ForeignKey linking to the `User` model, representing the user who created the template.
        - `organization`: ForeignKey linking to the `Organization` model, representing the organization associated with the template.
        - `template_text`: The text content of the message template.
        - `created_at`: Timestamp for when the template was created.
        - `updated_at`: Timestamp for when the template was last updated.
    - Meta:
        - `verbose_name`: "Message Template"
        - `verbose_name_plural`: "Message Templates"
        - `ordering`: Orders templates by creation date in descending order.
        - `indexes`: Indexes on various fields, including combinations of `user`, `organization`, `created_at`, and `template_text` for optimized queries.
    """

    # Foreign keys
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE)
    template_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Message Template"
        verbose_name_plural = "Message Templates"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "organization", "created_at"]),
            models.Index(fields=["user", "organization"]),
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["template_text"]),
            models.Index(fields=["user", "organization", "template_text"]),
            models.Index(fields=["user", "template_text"]),
            models.Index(fields=["organization", "template_text"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.organization} - {self.template_text}"
