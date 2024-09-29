#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: custom_function_models.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:01:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


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
