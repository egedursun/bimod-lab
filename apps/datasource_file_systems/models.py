
from django.db import models
from apps._services.file_systems.file_systems_executor import FileSystemsExecutor

# Create your models here.


SSH_CONNECTION_DEFAULT_BANNER_TIMEOUT = 200

DATASOURCE_FILE_SYSTEMS_OS_TYPES = [
    ('linux', 'Linux'),
    ('macos', 'MacOS'),
]


class DataSourceFileSystemsOsTypeNames:
    LINUX = 'linux'
    MACOS = 'macos'


class DataSourceFileSystem(models.Model):
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
