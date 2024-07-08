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

    def __str__(self):
        return f"{self.user} - {self.organization} - {self.template_text}"
