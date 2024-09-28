from django.db import models

from apps.mm_apis.utils import CUSTOM_API_AUTHENTICATION_TYPES


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
