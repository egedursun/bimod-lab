import random

import boto3
from django.db import models

from config import settings


class ExpertNetworkAssistantReference(models.Model):
    network = models.ForeignKey("ExpertNetwork", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    context_instructions = models.TextField(default="", blank=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='expert_network_assistant_references_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='expert_network_assistant_references_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.network.name + " - " + self.assistant.name

    class Meta:
        verbose_name = "Expert Network Assistant Reference"
        verbose_name_plural = "Expert Network Assistant References"
        ordering = ["-created_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=["network"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["context_instructions"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),

            # Two-field composite indexes
            models.Index(fields=["network", "assistant"]),
            models.Index(fields=["network", "context_instructions"]),
            models.Index(fields=["network", "created_by_user"]),
            models.Index(fields=["network", "last_updated_by_user"]),
            models.Index(fields=["network", "created_at"]),
            models.Index(fields=["network", "updated_at"]),
            models.Index(fields=["assistant", "context_instructions"]),
            models.Index(fields=["assistant", "created_by_user"]),
            models.Index(fields=["assistant", "last_updated_by_user"]),
            models.Index(fields=["assistant", "created_at"]),
            models.Index(fields=["assistant", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),

            # Three-field composite indexes
            models.Index(fields=["network", "assistant", "context_instructions"]),
            models.Index(fields=["network", "assistant", "created_by_user"]),
            models.Index(fields=["network", "assistant", "last_updated_by_user"]),
            models.Index(fields=["network", "assistant", "created_at"]),
            models.Index(fields=["network", "assistant", "updated_at"]),
            models.Index(fields=["network", "context_instructions", "created_at"]),
            models.Index(fields=["network", "context_instructions", "updated_at"]),
            models.Index(fields=["network", "created_by_user", "created_at"]),
            models.Index(fields=["network", "created_by_user", "updated_at"]),
            models.Index(fields=["network", "last_updated_by_user", "created_at"]),
            models.Index(fields=["network", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["assistant", "context_instructions", "created_at"]),
            models.Index(fields=["assistant", "context_instructions", "updated_at"]),
            models.Index(fields=["assistant", "created_by_user", "created_at"]),
            models.Index(fields=["assistant", "created_by_user", "updated_at"]),
            models.Index(fields=["assistant", "last_updated_by_user", "created_at"]),
            models.Index(fields=["assistant", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),
        ]


class ExpertNetwork(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='expert_networks', null=True, blank=True)
    name = models.CharField(max_length=255)
    meta_description = models.TextField(default="", blank=True)

    assistant_references = models.ManyToManyField("ExpertNetworkAssistantReference", related_name='networks')

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='expert_networks_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='expert_networks_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expert Network"
        verbose_name_plural = "Expert Networks"
        ordering = ["-created_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=["name"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),

            # Two-field composite indexes
            models.Index(fields=["name", "created_at"]),
            models.Index(fields=["name", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),

            # Three-field composite indexes
            models.Index(fields=["name", "created_by_user", "created_at"]),
            models.Index(fields=["name", "created_by_user", "updated_at"]),
            models.Index(fields=["name", "last_updated_by_user", "created_at"]),
            models.Index(fields=["name", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),

            # Four-field composite indexes
            models.Index(fields=["name", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["name", "last_updated_by_user", "created_at", "updated_at"]),
        ]


class LeanAssistant(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='lean_assistants')
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='lean_assistants')
    name = models.CharField(max_length=255)
    instructions = models.TextField(default="", blank=True)

    lean_assistant_image_save_path = 'lean_assistant_images/%Y/%m/%d/'
    lean_assistant_image = models.ImageField(upload_to=lean_assistant_image_save_path, blank=True, max_length=1000, null=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='lean_assistants_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='lean_assistants_updated_by_user')

    expert_networks = models.ManyToManyField("ExpertNetwork", related_name='lean_assistants', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.organization.name + " - " + self.llm_model.nickname

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        s3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        base_s3_url = f"https://{bucket_name}.s3.amazonaws.com/"
        print(f"[LeanAssistant.save] Saving the lean assistant: {self.name}.")
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        s3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        print(f"[LeanAssistant.delete] Deleting the lean assistant: {self.name}.")

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
                print(f"[LeanAssistant.delete] There has been an error in deleting the lean assistant directory {full_uri}: {e}")
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Lean Assistant"
        verbose_name_plural = "Lean Assistants"
        ordering = ["-created_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=["organization"]),
            models.Index(fields=["llm_model"]),
            models.Index(fields=["name"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),

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
        ]

    @staticmethod
    def generate_random_name_suffix():
        print(f"[LeanAssistant.generate_random_name_suffix] Generating a random name suffix.")
        return f"{str(random.randint(1_000_000_000, 9_999_999_999))}"

