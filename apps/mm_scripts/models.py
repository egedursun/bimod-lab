"""
Module Overview: This module defines models related to custom scripts within an assistant-based application. It includes models for storing script references, script details, and associated metadata such as categories, content, and step guides.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
"""

from django.db import models

# not used for now
SCRIPT_SOURCES = {
    "internal": "internal", "external": "external",
}


class CustomScriptReference(models.Model):
    """
    CustomScriptReference Model:
    - Purpose: Represents a reference to a custom script associated with a specific assistant, storing information about the script source and the user who created the reference.
    - Key Fields:
        - `custom_script`: ForeignKey linking to the `CustomScript` model.
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `script_source`: A field indicating whether the script is internal or external.
        - `created_by_user`: ForeignKey linking to the `User` who created the script reference.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Meta:
        - `verbose_name`: "Custom Script Reference"
        - `verbose_name_plural`: "Custom Script References"
        - `unique_together`: Ensures that each combination of `custom_script` and `assistant` is unique.
        - `indexes`: Indexes on various fields for optimized queries.
    """

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
    """
    CustomScript Model:
    - Purpose: Represents a custom script, storing details such as the name, description, categories, content, and associated metadata like step guides and script references.
    - Key Fields:
        - `is_public`: Boolean flag indicating whether the script is publicly accessible.
        - `categories`: JSONField for storing categories associated with the script.
        - `name`: The name of the custom script.
        - `description`: A description of the script.
        - `script_content`: TextField for storing the actual content of the script.
        - `script_step_guide`: JSONField for storing a step-by-step guide related to the script.
        - `custom_script_references`: ManyToManyField linking to `CustomScriptReference` instances associated with the script.
        - `script_picture`: ImageField for storing an optional picture associated with the script.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the `User` who created the script.
        - `is_featured`: Boolean flag indicating whether the script is featured.
    - Meta:
        - `verbose_name`: "Custom Script"
        - `verbose_name_plural`: "Custom Scripts"
        - `indexes`: Indexes on various fields for optimized queries.
    """

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
