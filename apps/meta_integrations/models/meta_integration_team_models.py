#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_integration_team_models.py
#  Last Modified: 2024-11-06 17:49:26
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 17:49:27
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
from config import settings


class MetaIntegrationTeam(models.Model):
    meta_integration_category = models.ForeignKey('MetaIntegrationCategory', on_delete=models.CASCADE, null=False,
                                                  blank=False)
    tags = models.JSONField(null=True, blank=True)
    meta_integration_name = models.CharField(max_length=1000, null=False, blank=False)
    meta_integration_description = models.TextField(null=True, blank=True)
    meta_integration_team_image = models.ImageField(upload_to='meta_integration_team_images/%Y/%m/%d/',
                                                    null=True, blank=True)

    integration_assistants = models.ManyToManyField('integrations.AssistantIntegration', blank=True,
                                                    related_name='meta_integration_teams')

    #################################################################################################################
    # OTHER FIELDS THAT ARE NEEDED (ON CREATION / INTEGRATION)
    #################################################################################################################
    # i. Organization -> will be taken from the user
    # ii. LLM Model -> will be taken from the user
    # iii. Management Type -> will be taken from the user
    #################################################################################################################

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meta_integration_name

    class Meta:
        verbose_name = 'Meta Integration Team'
        verbose_name_plural = 'Meta Integration Teams'
        indexes = [
            models.Index(fields=['meta_integration_name']),
            models.Index(fields=['meta_integration_category']),
            models.Index(fields=['tags']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def save(self, *args, **kwargs):
        # Check if the image field is empty
        if not self.meta_integration_team_image:
            static_image_directory = os.path.join(settings.STATIC_ROOT, 'img', 'integration-teams-avatars')
            available_images = [f for f in os.listdir(static_image_directory) if f.endswith(('png', 'jpg', 'jpeg'))]
            if available_images:
                random_image = random.choice(available_images)
                random_image_path = os.path.join(static_image_directory, random_image)
                unique_filename = f'meta_integration_team_images/{uuid.uuid4()}.png'
                with open(random_image_path, 'rb') as img_file:
                    default_storage.save(unique_filename, File(img_file))
                self.meta_integration_team_image.name = unique_filename
        super(MetaIntegrationTeam, self).save(*args, **kwargs)
