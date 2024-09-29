#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: custom_script_models.py
#  Last Modified: 2024-09-27 19:28:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:03:03
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


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
