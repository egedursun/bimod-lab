#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: file_system_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.db import models

from apps._services.file_systems.file_systems_executor import FileSystemsExecutor
from apps.datasource_file_systems.utils import DATASOURCE_FILE_SYSTEMS_OS_TYPES


class DataSourceFileSystem(models.Model):
    """
    DataSourceFileSystem Model:
    - Purpose: Represents a remote file system connection accessible via SSH, including details such as the OS type, SSH credentials, and data retrieval settings.
    - Key Fields:
        - `assistant`: ForeignKey linking to the `Assistant` model, representing the assistant associated with this file system connection.
        - `os_type`: The operating system type of the remote file system (e.g., Linux, MacOS).
        - `name`: The name of the file system connection.
        - `description`: A brief description of the connection.
        - `host_url`: The URL or IP address of the remote file system.
        - `port`: The port number for the SSH connection (default is 22).
        - `username`, `password`: Credentials for SSH login.
        - `file_directory_tree`: A text representation of the file directory structure.
        - `os_read_limit_tokens`: Limit for the number of tokens to read from the OS.
        - `is_read_only`: Boolean flag to indicate if the connection is read-only.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the user who created the file system connection.
    - Methods:
        - `save()`: Overridden to construct the SSH connection URI and update the file directory tree using `FileSystemsExecutor` before saving the model.
    """

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE,
                                  related_name='data_source_file_systems',
                                  default=None, null=True)
    os_type = models.CharField(max_length=50, choices=DATASOURCE_FILE_SYSTEMS_OS_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # SSH Connection Parameters
    host_url = models.CharField(max_length=255)
    port = models.IntegerField(default=22)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    # Data
    file_directory_tree = models.TextField(blank=True, null=True)

    # Retrieval parameters
    os_read_limit_tokens = models.IntegerField(default=10_000)
    is_read_only = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='data_source_file_systems',
                                        default=None, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Data Source File Systems'
        verbose_name = 'Data Source File System'
        indexes = [
            models.Index(fields=['assistant', 'os_type', 'name']),
            models.Index(fields=['assistant', 'os_type', 'created_at']),
            models.Index(fields=['assistant', 'os_type', 'updated_at']),
            models.Index(fields=['assistant', 'os_type', 'name', 'created_at']),
            models.Index(fields=['assistant', 'os_type', 'name', 'updated_at']),
        ]

    def __str__(self):
        return self.name + ' (' + self.os_type + ')' + ' - ' + self.host_url + ':' + str(self.port)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.ssh_connection_uri = f"{self.username}@{self.host_url}"
        schema_str = FileSystemsExecutor(self).schema_str
        self.file_directory_tree = schema_str
        super().save(force_insert, force_update, using, update_fields)
