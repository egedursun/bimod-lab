from django.db import models

# not used for now
SCRIPT_SOURCES = {
    "internal": "internal", "external": "external",
}


class CustomScriptReference(models.Model):
    custom_script = models.ForeignKey("CustomScript", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    script_source = models.CharField(max_length=255, default="internal", blank=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_script.name + " - " + self.assistant.name + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom Script Reference"
        verbose_name_plural = "Custom Script References"
        unique_together = [["custom_script", "assistant"]]
        indexes = [
            models.Index(fields=["custom_script", "assistant"]),
            models.Index(fields=["assistant", "custom_script", "created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["custom_script"]),
            models.Index(fields=["created_by_user"]),
        ]


CUSTOM_SCRIPT_CATEGORIES = [
    ("data", "Data"),
    ("aiml", "AI/ML"),
    ("media", "Media"),
    ("automation", "Automation"),
    ("apis", "APIs"),
    ("finance", "Finance"),
    ("commerce", "Commerce"),
    ("support", "Support"),
    ("social", "Social"),
    ("iot", "IoT"),
    ("health", "Health"),
    ("legal", "Legal"),
    ("education", "Education"),
    ("travel", "Travel"),
    ("security", "Security"),
    ("privacy", "Privacy"),
    ("entertainment", "Entertainment"),
    ("productivity", "Productivity"),
    ("utilities", "Utilities"),
    ("miscellaneous", "Miscellaneous"),
]


class CustomScript(models.Model):
    is_public = models.BooleanField(default=False)
    categories = models.JSONField(default=list, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # script-specific fields
    script_content = models.TextField(blank=True)
    script_step_guide = models.JSONField(default=list, blank=True)

    custom_script_references = models.ManyToManyField("CustomScriptReference", blank=True)
    script_picture = models.ImageField(upload_to="custom_scripts/%YYYY/%mm/%dd/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom Script"
        verbose_name_plural = "Custom Scripts"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_public"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["name", "is_public"]),
        ]
