#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_integration_models.py
#  Last Modified: 2024-11-05 19:22:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-05 19:22:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import os
import random
import uuid

from django.core.files import File
from django.core.files.storage import default_storage
from django.db import models

from apps.assistants.utils import MultiStepReasoningCapabilityChoicesNames
from config import settings


class AssistantIntegration(models.Model):
    # (On Creation)
    integration_category = models.ForeignKey('AssistantIntegrationCategory', on_delete=models.CASCADE)
    tags = models.JSONField(null=True, blank=True)
    integration_name = models.CharField(max_length=1000)  # Important
    integration_description = models.TextField(null=True, blank=True)  # Important
    integration_instructions = models.TextField(null=True, blank=True)  # Important
    integration_audience = models.CharField(max_length=1000, null=True, blank=True)  # Important
    integration_tone = models.CharField(max_length=1000, null=True, blank=True)  # Important
    integration_assistant_image = models.ImageField(upload_to='integration_assistant_images/%Y/%m/%d/',
                                                    null=True, blank=True)

    # Multi-modalities (Optional) (After Creation)
    integration_multi_step_reasoning = models.CharField()  # Important
    integration_context_overflow_strategy = models.CharField(default="forget", max_length=1100)  # Optional field
    integration_response_language = models.CharField(default="auto", max_length=1000)  # Optional field
    integration_custom_functions = models.ManyToManyField('mm_functions.CustomFunction', blank=True)
    integration_custom_apis = models.ManyToManyField('mm_apis.CustomAPI', blank=True)
    integration_custom_scripts = models.ManyToManyField('mm_scripts.CustomScript', blank=True)
    integration_response_template = models.TextField(default="")  # Optional field
    integration_glossary = models.JSONField(default=dict, blank=True)  # Optional field
    ner_integration = models.ForeignKey("data_security.NERIntegration", on_delete=models.SET_NULL,
                                        related_name='assistant_integrations', null=True, blank=True)
    project_items = models.ManyToManyField('projects.ProjectItem', blank=True, related_name='assistant_integrations')

    # Overridable Configurations (After Creation)
    integration_time_awareness = models.BooleanField(default=True)  # Can be overridden
    integration_location_awareness = models.BooleanField(default=True)  # Can be overridden
    integration_max_retries = models.IntegerField(default=5)  # Can be overridden
    integration_max_tool_retries = models.IntegerField(default=5)  # Can be overridden
    integration_max_tool_pipelines = models.IntegerField(default=5)  # Can be overridden
    integration_max_message_memory = models.IntegerField(default=5)  # Can be overridden
    integration_image_generation_capability = models.BooleanField(default=True)  # Can be overridden

    # Metadata (On Creation + On Update)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #################################################################################################################
    #  USER DEFINED PROPERTIES
    #################################################################################################################
    # Configuration: organization, llm_model
    #################################################################################################################

    def __str__(self):
        return self.integration_name + ' - ' + self.integration_category.category_name

    class Meta:
        verbose_name = 'Assistant Integration'
        verbose_name_plural = 'Assistant Integrations'
        ordering = ['-integration_name']
        indexes = [
            models.Index(fields=['integration_name']),
            models.Index(fields=['integration_name', 'integration_category']),
            models.Index(fields=['integration_name', 'integration_category', 'integration_audience']),
            models.Index(fields=['integration_name', 'integration_category', 'integration_tone']),
            models.Index(fields=['integration_name', 'integration_category', 'integration_multi_step_reasoning']),
            models.Index(fields=['integration_name', 'integration_category', 'integration_time_awareness']),
            models.Index(fields=['integration_name', 'integration_category', 'integration_location_awareness']),
            models.Index(fields=['integration_name', 'integration_category', 'integration_max_retries']),
            models.Index(fields=['integration_name', 'integration_category', 'integration_max_tool_retries']),
        ]

    def save(self, *args, **kwargs):
        # Check if the image field is empty
        self.integration_multi_step_reasoning = MultiStepReasoningCapabilityChoicesNames.HIGH_PERFORMANCE
        if not self.integration_assistant_image:
            static_image_directory = os.path.join(settings.STATIC_ROOT, 'img', 'integration-assistant-avatars')
            available_images = [f for f in os.listdir(static_image_directory) if f.endswith(('png', 'jpg', 'jpeg'))]
            if available_images:
                random_image = random.choice(available_images)
                random_image_path = os.path.join(static_image_directory, random_image)
                unique_filename = f'integration_assistant_images/{uuid.uuid4()}.png'
                with open(random_image_path, 'rb') as img_file:
                    default_storage.save(unique_filename, File(img_file))
                self.integration_assistant_image.name = unique_filename
        super(AssistantIntegration, self).save(*args, **kwargs)
