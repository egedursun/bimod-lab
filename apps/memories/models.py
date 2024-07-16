from django.db import models


# Create your models here.


MEMORY_TYPE = [
    ("user-specific", "User-Specific"),
    ("assistant-specific", "Assistant-Specific"),
]


class AssistantMemory(models.Model):
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
