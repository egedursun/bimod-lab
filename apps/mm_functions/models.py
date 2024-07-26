from django.db import models


FUNCTION_IO_FIELDS_FORMAT = {
    "name": "string",
    "description": "string",
    "type": "string",
    "required": "boolean",
}

FUNCTION_PACKAGES_FORMAT = {
    "name": "string",
    "version": "string",
}


# not used for now
FUNCTION_SOURCES = {
    "internal": "internal",
    "external": "external",
}


# Create your models here.


class CustomFunctionReference(models.Model):
    custom_function = models.ForeignKey("CustomFunction", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    function_source = models.CharField(max_length=255, default="internal", blank=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_function.name + " - " + self.assistant.name + " - " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom Function Reference"
        verbose_name_plural = "Custom Function References"
        unique_together = [["custom_function", "assistant"]]
        indexes = [
            models.Index(fields=["custom_function", "assistant"]),
            models.Index(fields=["assistant", "custom_function", "created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["custom_function"]),
            models.Index(fields=["created_by_user"]),
        ]


CUSTOM_FUNCTION_CATEGORIES = [
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


class CustomFunction(models.Model):
    is_public = models.BooleanField(default=False)
    categories = models.JSONField(default=list, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField()

    packages = models.JSONField(default=list, blank=True)
    input_fields = models.JSONField(default=list, blank=True)
    output_fields = models.JSONField(default=list, blank=True)
    code_text = models.TextField(default="", blank=True)

    custom_function_references = models.ManyToManyField("CustomFunctionReference", blank=True)
    function_picture = models.ImageField(upload_to="custom_functions/%YYYY/%mm/%dd/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom Function"
        verbose_name_plural = "Custom Functions"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_public"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["name", "is_public"]),
        ]

