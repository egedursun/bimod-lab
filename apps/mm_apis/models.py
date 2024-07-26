from django.db import models


# Create your models here.


# not used for now
API_SOURCES = {
    "internal": "internal",
    "external": "external",
}


# Create your models here.


class CustomAPIReference(models.Model):
    custom_api = models.ForeignKey("CustomAPI", on_delete=models.CASCADE)
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
    is_public = models.BooleanField(default=False)
    categories = models.JSONField(default=list, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField()

    authentication_type = models.CharField(max_length=5000, default="None", choices=CUSTOM_API_AUTHENTICATION_TYPES)
    authentication_token = models.CharField(max_length=5000, default="", blank=True)
    base_url = models.CharField(max_length=5000, default="")

    """ {"Some Endpoint Name" = {
        "description": "Some natural language description.",
        "path": "/users",
        "method": "POST",
        "header_params": ["Authorization"],
        "path_params": [], "query_params": [],
        "body_params": ["name", "email", "password"] },
    "Other Endpoint Name" = { ... }, }
    """
    endpoints = models.JSONField(default=dict, blank=True)
    """Structure definition above."""

    custom_api_references = models.ManyToManyField("CustomAPIReference", blank=True)
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
