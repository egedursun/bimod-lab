from django.db import models


# Create your models here.


class MessageTemplate(models.Model):
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
