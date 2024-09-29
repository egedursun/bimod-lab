#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: assistant_models.py
#  Last Modified: 2024-09-26 18:15:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:18:02
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import random

import boto3
from django.db import models

from apps.assistants.utils import ASSISTANT_RESPONSE_LANGUAGES, CONTEXT_OVERFLOW_STRATEGY, VECTORIZERS
from config import settings


class Assistant(models.Model):
    """
    Assistant Model:
    - Purpose: Represents a virtual assistant with customizable settings, including language, context management, and storage directories.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` model.
        - `llm_model`: ForeignKey linking to the `LLMCore` model.
        - `name`: The name of the assistant.
        - `description`, `instructions`, `response_template`: Fields for storing assistant-specific text configurations.
        - `audience`, `tone`: Characterizes the assistant's communication style.
        - `response_language`: Defines the assistant's response language.
        - `max_retry_count`: Number of retry attempts for tools.
        - `tool_max_attempts_per_instance`, `tool_max_chains`: Limits on tool usage.
        - `glossary`: JSON field for storing glossary terms.
        - `time_awareness`, `place_awareness`: Booleans for enabling time and place awareness.
        - `assistant_image`: Image field for storing the assistant's image.
        - `memories`: ManyToManyField linking to the `AssistantMemory` model.
        - `context_overflow_strategy`: Defines how to handle context overflow.
        - `max_context_messages`: Maximum number of context messages allowed.
        - `vectorizer_name`: Defines the vectorizer used for the assistant.
        - `vectorizer_api_key`: API key for the vectorizer.
        - `document_base_directory`, `storages_base_directory`, `ml_models_base_directory`: S3 directories for storing
            assistant-related files.
        - `created_by_user`, `last_updated_by_user`: ForeignKeys linking to the user who created or last updated the
            assistant.
        - `image_generation_capability`: Boolean for enabling image generation.
        - `created_at`, `updated_at`: Timestamps for assistant creation and last update.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='assistants')
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='assistants')
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    instructions = models.TextField(default="", blank=True)
    response_template = models.TextField(default="", blank=True)
    audience = models.CharField(max_length=1000)
    tone = models.CharField(max_length=1000)
    response_language = models.CharField(max_length=10, choices=ASSISTANT_RESPONSE_LANGUAGES, default="auto")
    max_retry_count = models.IntegerField(default=3)

    tool_max_attempts_per_instance = models.IntegerField(default=3)
    tool_max_chains = models.IntegerField(default=3)

    glossary = models.JSONField(default=dict, blank=True)

    time_awareness = models.BooleanField(default=True)
    place_awareness = models.BooleanField(default=True)

    # assistant image
    assistant_image_save_path = 'assistant_images/%Y/%m/%d/'
    assistant_image = models.ImageField(upload_to=assistant_image_save_path, blank=True, max_length=1000, null=True)
    memories = models.ManyToManyField("memories.AssistantMemory", related_name='assistants', blank=True)

    context_overflow_strategy = models.CharField(max_length=100, choices=CONTEXT_OVERFLOW_STRATEGY, default="forget")
    max_context_messages = models.IntegerField(default=25)
    vectorizer_name = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai", null=True,
                                       blank=True)

    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)
    document_base_directory = models.CharField(max_length=1000, null=True, blank=True)
    storages_base_directory = models.CharField(max_length=1000, null=True, blank=True)
    ml_models_base_directory = models.CharField(max_length=1000, null=True, blank=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='assistants_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='assistants_updated_by_user')

    image_generation_capability = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Data Security Integrations
    ner_integration = models.ForeignKey("data_security.NERIntegration", on_delete=models.SET_NULL,
                                        related_name='assistants', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        s3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        base_s3_url = f"https://{bucket_name}.s3.amazonaws.com/"
        print(f"[Assistant.save] Saving the assistant: {self.name}.")

        if self.document_base_directory is None:
            try:
                dir_name = f"documents/{str(self.organization.id)}/{str(self.llm_model.id)}/{self.generate_random_name_suffix()}/"
                full_uri = f"{base_s3_url}{dir_name}"
                s3_client.put_object(Bucket=bucket_name, Key=f"{dir_name}/")
                self.document_base_directory = full_uri
            except Exception as e:
                print(f"[Assistant.save] There has been an error in creating the document directory: {e}")

        if self.storages_base_directory is None:
            try:
                dir_name = f"storages/{str(self.organization.id)}/{str(self.llm_model.id)}/{self.generate_random_name_suffix()}/"
                full_uri = f"{base_s3_url}{dir_name}"
                s3_client.put_object(Bucket=bucket_name, Key=f"{dir_name}/")
                self.storages_base_directory = full_uri
            except Exception as e:
                print(f"[Assistant.save] There has been an error in creating the storages directory: {e}")

        if self.ml_models_base_directory is None:
            try:
                dir_name = f"ml_models/{str(self.organization.id)}/{str(self.llm_model.id)}/{self.generate_random_name_suffix()}/"
                full_uri = f"{base_s3_url}{dir_name}"
                s3_client.put_object(Bucket=bucket_name, Key=f"{dir_name}/")
                self.ml_models_base_directory = full_uri
            except Exception as e:
                print(f"[Assistant.save] There has been an error in creating the ml_models directory: {e}")

        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        s3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        print(f"[Assistant.delete] Deleting the assistant: {self.name}.")

        def delete_s3_directory(full_uri):
            try:
                dir_name = full_uri.replace(f"https://{bucket_name}.s3.amazonaws.com/", "")
                paginator = s3_client.get_paginator('list_objects_v2')
                pages = paginator.paginate(Bucket=bucket_name, Prefix=dir_name)
                for page in pages:
                    if 'Contents' in page:
                        delete_keys = {'Objects': [{'Key': obj['Key']} for obj in page['Contents']]}
                        s3_client.delete_objects(Bucket=bucket_name, Delete=delete_keys)
            except Exception as e:
                print(f"[Assistant.delete] There has been an error in deleting the directory {full_uri}: {e}")

        if self.document_base_directory is not None:
            delete_s3_directory(self.document_base_directory)

        if self.storages_base_directory is not None:
            delete_s3_directory(self.storages_base_directory)

        if self.ml_models_base_directory is not None:
            delete_s3_directory(self.ml_models_base_directory)

        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Assistant"
        verbose_name_plural = "Assistants"
        ordering = ["-created_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=["organization"]),
            models.Index(fields=["llm_model"]),
            models.Index(fields=["name"]),
            models.Index(fields=["response_language"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["context_overflow_strategy"]),
            models.Index(fields=["vectorizer_name"]),

            # Two-field composite indexes
            models.Index(fields=["organization", "llm_model"]),
            models.Index(fields=["organization", "name"]),
            models.Index(fields=["organization", "created_by_user"]),
            models.Index(fields=["organization", "last_updated_by_user"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["organization", "updated_at"]),
            models.Index(fields=["llm_model", "name"]),
            models.Index(fields=["llm_model", "created_by_user"]),
            models.Index(fields=["llm_model", "last_updated_by_user"]),
            models.Index(fields=["llm_model", "created_at"]),
            models.Index(fields=["llm_model", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),

            # Three-field composite indexes
            models.Index(fields=["organization", "llm_model", "name"]),
            models.Index(fields=["organization", "llm_model", "created_by_user"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user"]),
            models.Index(fields=["organization", "llm_model", "created_at"]),
            models.Index(fields=["organization", "llm_model", "updated_at"]),
            models.Index(fields=["organization", "name", "created_at"]),
            models.Index(fields=["organization", "name", "updated_at"]),
            models.Index(fields=["organization", "created_by_user", "created_at"]),
            models.Index(fields=["organization", "created_by_user", "updated_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "created_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["llm_model", "name", "created_at"]),
            models.Index(fields=["llm_model", "name", "updated_at"]),
            models.Index(fields=["llm_model", "created_by_user", "created_at"]),
            models.Index(fields=["llm_model", "created_by_user", "updated_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "created_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),

            # Four-field composite indexes
            models.Index(fields=["organization", "llm_model", "name", "created_at"]),
            models.Index(fields=["organization", "llm_model", "name", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "created_by_user", "created_at"]),
            models.Index(fields=["organization", "llm_model", "created_by_user", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user", "created_at"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["organization", "name", "created_at", "updated_at"]),
            models.Index(fields=["organization", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "name", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "created_at", "updated_at"]),

            # Additional useful combinations
            models.Index(fields=["organization", "context_overflow_strategy"]),
            models.Index(fields=["organization", "vectorizer_name"]),
            models.Index(fields=["llm_model", "context_overflow_strategy"]),
            models.Index(fields=["llm_model", "vectorizer_name"]),
            models.Index(fields=["organization", "llm_model", "context_overflow_strategy"]),
            models.Index(fields=["organization", "llm_model", "vectorizer_name"]),
            models.Index(fields=["created_by_user", "context_overflow_strategy"]),
            models.Index(fields=["created_by_user", "vectorizer_name"]),
            models.Index(fields=["last_updated_by_user", "context_overflow_strategy"]),
            models.Index(fields=["last_updated_by_user", "vectorizer_name"]),
        ]

    @staticmethod
    def generate_random_name_suffix():
        print(f"[Assistant.generate_random_name_suffix] Generating a random name suffix.")
        return f"{str(random.randint(1_000_000_000, 9_999_999_999))}"
