"""
Module Overview: This module defines models related to custom APIs within an assistant-based application. It includes models for storing API references, API details, and associated metadata such as authentication types, categories, and endpoints.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
"""

from django.db import models


# not used for now
API_SOURCES = {
    "internal": "internal",
    "external": "external",
}


class CustomAPIReference(models.Model):
    """
    CustomAPIReference Model:
    - Purpose: Represents a reference to a custom API associated with a specific assistant, storing information about the API source and the user who created the reference.
    - Key Fields:
        - `custom_api`: ForeignKey linking to the `CustomAPI` model.
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `api_source`: A field indicating whether the API is internal or external.
        - `created_by_user`: ForeignKey linking to the `User` who created the API reference.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Meta:
        - `verbose_name`: "Custom API Reference"
        - `verbose_name_plural`: "Custom API References"
        - `unique_together`: Ensures that each combination of `custom_api` and `assistant` is unique.
        - `indexes`: Indexes on various fields for optimized queries.
    """

    custom_api = models.ForeignKey("CustomAPI", on_delete=models.CASCADE, related_name="custom_api_references")
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    api_source = models.CharField(max_length=255, default="internal", blank=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_api.name + " - " + self.assistant.name + " - " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom API Reference"
        verbose_name_plural = "Custom API References"
        unique_together = [["custom_api", "assistant"]]
        indexes = [
            models.Index(fields=["custom_api", "assistant"]),
            models.Index(fields=["assistant", "custom_api", "created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["custom_api"]),
            models.Index(fields=["created_by_user"]),
        ]


CUSTOM_API_CATEGORIES = [
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


CUSTOM_API_AUTHENTICATION_TYPES = [
    ("None", "None"),
    ("Bearer", "Bearer")
]


class AcceptedHTTPRequestMethods:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class CustomAPI(models.Model):
    """
    CustomAPI Model:
    - Purpose: Represents a custom API, storing details such as the name, description, authentication type, base URL, endpoints, and associated metadata like categories and whether the API is public or featured.
    - Key Fields:
        - `is_public`: Boolean flag indicating whether the API is publicly accessible.
        - `categories`: JSONField for storing categories associated with the API.
        - `name`: The name of the custom API.
        - `description`: A description of the API.
        - `authentication_type`: The type of authentication required (e.g., None, Bearer).
        - `authentication_token`: The token used for authentication if required.
        - `base_url`: The base URL for the API.
        - `endpoints`: JSONField for storing the structure of the API's endpoints.
        - `custom_api_references`: ManyToManyField linking to `CustomAPIReference` instances associated with the API.
        - `api_picture`: ImageField for storing an optional picture associated with the API.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the `User` who created the API.
        - `is_featured`: Boolean flag indicating whether the API is featured.
    - Meta:
        - `verbose_name`: "Custom API"
        - `verbose_name_plural`: "Custom APIs"
        - `indexes`: Indexes on various fields for optimized queries.
    """

    is_public = models.BooleanField(default=False)
    categories = models.JSONField(default=list, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField()

    authentication_type = models.CharField(max_length=5000, default="None", choices=CUSTOM_API_AUTHENTICATION_TYPES)
    authentication_token = models.CharField(max_length=5000, default="", blank=True)
    base_url = models.CharField(max_length=5000, default="")

    endpoints = models.JSONField(default=dict, blank=True)

    api_picture = models.ImageField(upload_to="custom_apis/%YYYY/%mm/%dd/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom API"
        verbose_name_plural = "Custom APIs"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_public"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["name", "is_public"]),
            models.Index(fields=["name", "is_featured"]),
        ]
