"""
Module Overview: This module defines models related to custom functions within an assistant-based application. It includes models for storing function references, function details, and associated metadata such as categories, packages, and input/output fields.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
"""

from django.db import models


FUNCTION_IO_FIELDS_FORMAT = {
    "name": "string", "description": "string", "type": "string", "required": "boolean",
}

FUNCTION_PACKAGES_FORMAT = {
    "name": "string", "version": "string",
}


# not used for now
FUNCTION_SOURCES = {
    "internal": "internal", "external": "external",
}


class CustomFunctionReference(models.Model):
    """
    CustomFunctionReference Model:
    - Purpose: Represents a reference to a custom function associated with a specific assistant, storing information about the function source and the user who created the reference.
    - Key Fields:
        - `custom_function`: ForeignKey linking to the `CustomFunction` model.
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `function_source`: A field indicating whether the function is internal or external.
        - `created_by_user`: ForeignKey linking to the `User` who created the function reference.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Meta:
        - `verbose_name`: "Custom Function Reference"
        - `verbose_name_plural`: "Custom Function References"
        - `unique_together`: Ensures that each combination of `custom_function` and `assistant` is unique.
        - `indexes`: Indexes on various fields for optimized queries.
    """
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE, null=True, blank=True, related_name="custom_function_references")
    custom_function = models.ForeignKey("CustomFunction", on_delete=models.CASCADE, related_name="custom_function_references")
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
    """
    CustomFunction Model:
    - Purpose: Represents a custom function, storing details such as the name, description, categories, packages, input/output fields, and associated metadata like code and secrets.
    - Key Fields:
        - `is_public`: Boolean flag indicating whether the function is publicly accessible.
        - `categories`: JSONField for storing categories associated with the function.
        - `name`: The name of the custom function.
        - `description`: A description of the function.
        - `packages`: JSONField for storing the packages required by the function.
        - `input_fields`, `output_fields`: JSONFields for storing the structure of input and output fields for the function.
        - `code_text`: TextField for storing the actual code of the function.
        - `secrets`: JSONField for storing any secrets required by the function.
        - `function_picture`: ImageField for storing an optional picture associated with the function.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the `User` who created the function.
        - `is_featured`: Boolean flag indicating whether the function is featured.
    - Meta:
        - `verbose_name`: "Custom Function"
        - `verbose_name_plural`: "Custom Functions"
        - `indexes`: Indexes on various fields for optimized queries.
    """

    is_public = models.BooleanField(default=False)
    categories = models.JSONField(default=list, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField()

    packages = models.JSONField(default=list, blank=True)
    input_fields = models.JSONField(default=list, blank=True)
    output_fields = models.JSONField(default=list, blank=True)
    code_text = models.TextField(default="", blank=True)
    secrets = models.JSONField(default=dict, blank=True)

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
