#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_models.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

import boto3
from django.db import models

from apps.assistants.utils import (
    AGENT_SPEECH_LANGUAGES,
    CONTEXT_MANAGEMENT_STRATEGY,
    MULTI_STEP_REASONING_CAPABILITY_CHOICE,
    generate_random_name_suffix
)

from config import settings

logger = logging.getLogger(__name__)


class Assistant(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='assistants'
    )

    llm_model = models.ForeignKey(
        'llm_core.LLMCore',
        on_delete=models.CASCADE,
        related_name='assistants'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    instructions = models.TextField(default="", blank=True)
    response_template = models.TextField(default="", blank=True)

    audience = models.CharField(max_length=1000)
    tone = models.CharField(max_length=1000)

    response_language = models.CharField(
        max_length=10,
        choices=AGENT_SPEECH_LANGUAGES,
        default="auto"
    )

    max_retry_count = models.IntegerField(default=3)
    tool_max_attempts_per_instance = models.IntegerField(default=3)
    tool_max_chains = models.IntegerField(default=3)

    glossary = models.JSONField(default=dict, blank=True)
    time_awareness = models.BooleanField(default=True)
    place_awareness = models.BooleanField(default=True)

    assistant_image_save_path = 'assistant_images/%Y/%m/%d/'

    assistant_image = models.ImageField(
        upload_to=assistant_image_save_path,
        blank=True,
        max_length=1000,
        null=True
    )

    memories = models.ManyToManyField(
        "memories.AssistantMemory",
        related_name='assistants',
        blank=True
    )

    context_overflow_strategy = models.CharField(
        max_length=100,
        choices=CONTEXT_MANAGEMENT_STRATEGY,
        default="forget"
    )

    max_context_messages = models.IntegerField(default=25)

    document_base_directory = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    storages_base_directory = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    ml_models_base_directory = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    created_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='assistants_created_by_user'
    )

    last_updated_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='assistants_updated_by_user'
    )

    image_generation_capability = models.BooleanField(default=True)

    multi_step_reasoning_capability_choice = models.CharField(
        max_length=100,
        choices=MULTI_STEP_REASONING_CAPABILITY_CHOICE,
        default="none"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ner_integration = models.ForeignKey(
        "data_security.NERIntegration",
        on_delete=models.SET_NULL,
        related_name='assistants',
        null=True,
        blank=True
    )

    project_items = models.ManyToManyField(
        "projects.ProjectItem",
        related_name='assistants',
        blank=True
    )

    is_beamguard_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        s3c = boto3.client('s3')

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        bucket_root_url = f"https://{bucket}.s3.amazonaws.com/"

        if self.document_base_directory is None:

            try:
                dir_name = f"documents/{str(self.organization.id)}/{str(self.llm_model.id)}/{generate_random_name_suffix()}/"
                f_uri = f"{bucket_root_url}{dir_name}"
                s3c.put_object(Bucket=bucket, Key=f"{dir_name}/")
                self.document_base_directory = f_uri

            except Exception as e:
                logger.error(f"Error while creating document base directory: {e}")

        if self.storages_base_directory is None:

            try:
                dir_name = f"storages/{str(self.organization.id)}/{str(self.llm_model.id)}/{generate_random_name_suffix()}/"
                f_uri = f"{bucket_root_url}{dir_name}"

                s3c.put_object(
                    Bucket=bucket,
                    Key=f"{dir_name}/"
                )

                self.storages_base_directory = f_uri

            except Exception as e:
                logger.error(f"Error while creating storages base directory: {e}")

        if self.ml_models_base_directory is None:

            try:
                dir_name = f"ml_models/{str(self.organization.id)}/{str(self.llm_model.id)}/{generate_random_name_suffix()}/"
                f_uri = f"{bucket_root_url}{dir_name}"

                s3c.put_object(
                    Bucket=bucket,
                    Key=f"{dir_name}/"
                )

                self.ml_models_base_directory = f_uri

            except Exception as e:
                logger.error(f"Error while creating ml models base directory: {e}")

        logger.info(f"Assistant has been created for organization.")

        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def delete(
        self,
        using=None,
        keep_parents=False
    ):
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        def delete_s3_directory(full_uri):

            try:
                dir_name = full_uri.replace(f"https://{bucket}.s3.amazonaws.com/", "")
                paginator = s3c.get_paginator('list_objects_v2')

                pages = paginator.paginate(
                    Bucket=bucket,
                    Prefix=dir_name
                )

                for page in pages:
                    if 'Contents' in page:
                        delete_keys = {
                            'Objects': [
                                {
                                    'Key': obj['Key']} for obj in page['Contents']
                            ]
                        }

                        s3c.delete_objects(
                            Bucket=bucket,
                            Delete=delete_keys
                        )

                logger.info(f"Deleted s3 directory: {full_uri}")

            except Exception as e:
                logger.error(f"Error while deleting s3 directory: {e}")

        if self.document_base_directory is not None:
            delete_s3_directory(self.document_base_directory)

        if self.storages_base_directory is not None:
            delete_s3_directory(self.storages_base_directory)

        if self.ml_models_base_directory is not None:
            delete_s3_directory(self.ml_models_base_directory)

        logger.info(f"Assistant has been deleted for organization.")
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Assistant"
        verbose_name_plural = "Assistants"
        ordering = ["-created_at"]

        unique_together = [
            [
                "organization",
                "name"
            ],
        ]

        indexes = [
            models.Index(fields=[
                "organization"
            ]),
            models.Index(fields=[
                "llm_model"
            ]),
            models.Index(fields=[
                "name"
            ]),
            models.Index(fields=[
                "response_language"
            ]),
            models.Index(fields=[
                "created_by_user"
            ]),
            models.Index(fields=[
                "last_updated_by_user"
            ]),
            models.Index(fields=[
                "created_at"
            ]),
            models.Index(fields=[
                "updated_at"
            ]),
            models.Index(fields=[
                "organization",
                "llm_model"
            ]),
            models.Index(fields=[
                "organization",
                "name"
            ]),
            models.Index(fields=[
                "organization",
                "created_at"
            ]),
            models.Index(fields=[
                "llm_model",
                "created_at"
            ]),
            models.Index(fields=[
                "organization",
                "created_by_user"
            ]),
            models.Index(fields=[
                "created_by_user",
                "created_at"
            ]),
            models.Index(fields=[
                "organization",
                "llm_model",
                "name"
            ]),
            models.Index(fields=[
                "organization",
                "llm_model",
                "created_by_user",
                "created_at"
            ]),
            models.Index(fields=[
                "organization",
                "llm_model",
                "updated_at"
            ]),
        ]
