"""
Module Overview: This module defines models for managing media storage connections and items in an assistant-based application. It includes configurations for media categories, file types, and the handling of media storage connections and items, with integration to storage services like AWS S3.

Dependencies:
- `os`, `random`, `shutil`: Python standard libraries for file and directory operations.
- `boto3`: Used for interacting with AWS S3 to manage storage directories and files.
- `paramiko`: Used for SSH-related tasks.
- `django.db.models`: Django's ORM for defining database models.
- `slugify`: Used to generate URL-friendly slugs for file and directory names.
- `config.settings`: Application settings, particularly for accessing media-related configurations.
- `.tasks.upload_file_to_storage`: Asynchronous task for uploading files to storage.
"""

import os
import random

import boto3
from django.db import models
from slugify import slugify

from config.settings import MEDIA_URL
from .tasks import upload_file_to_storage


MEDIA_CATEGORIES = (
    ('image', 'Image'),
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('compressed', 'Compressed'),
    ('code', 'Code'),
    ('data', 'Data'),
)


class MediaCategoriesNames:
    Image = 'image'
    Audio = 'audio'
    Video = 'video'
    Compressed = 'compressed'
    Code = 'code'
    Data = 'data'


MEDIA_FILE_TYPES = (
    # Image Files
    ('jpg', 'JPEG'),
    ('png', 'PNG'),
    ('gif', 'GIF'),
    ('svg', 'SVG'),
    ('bmp', 'BMP'),
    ('tiff', 'TIFF'),
    # Audio Files
    ('mp3', 'MP3'),
    ('wav', 'WAV'),
    ('flac', 'FLAC'),
    ('aac', 'AAC'),
    ('ogg', 'OGG'),
    # Video Files
    ('mp4', 'MP4'),
    ('avi', 'AVI'),
    ('mkv', 'MKV'),
    ('mov', 'MOV'),
    # Compressed Files
    ('zip', 'ZIP'),
    ('rar', 'RAR'),
    ('tar', 'TAR'),
    # Code Files
    ('py', 'Python'),
    ('js', 'JavaScript'),
    ('ts', 'TypeScript'),
    ('php', 'PHP'),
    ('css', 'CSS'),
    ('html', 'HTML'),
    ('java', 'Java'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('h', 'C-Header'),
    ('sh', 'Shell'),
    ('go', 'Go'),
    ('dart', 'Dart'),
    # Data Configuration files
    ('yml', 'YML'),
    ('yaml', 'YAML'),
    ('sql', 'SQL'),
    ('pkl', 'Pickle'),
    ('csv', 'CSV'),
    ('xlsx', 'XLSX'),
    ('json', 'JSON'),
    ('xml', 'XML'),
    ('tsv', 'TSV'),
    ('docx', 'DOCX'),
    ('pptx', 'PPTX'),
    ('pdf', 'PDF'),
    ('txt', 'TXT'),
)


class MediaFileTypesNames:
    class Image:
        JPEG = 'jpg'
        PNG = 'png'
        GIF = 'gif'
        SVG = 'svg'
        BMP = 'bmp'
        TIFF = 'tiff'

    class Audio:
        MP3 = 'mp3'
        WAV = 'wav'
        FLAC = 'flac'
        AAC = 'aac'
        OGG = 'ogg'

    class Video:
        MP4 = 'mp4'
        AVI = 'avi'
        MKV = 'mkv'
        MOV = 'mov'

    class Compressed:
        ZIP = 'zip'
        RAR = 'rar'
        TAR = 'tar'

    class Code:
        Python = 'py'
        JavaScript = 'js'
        TypeScript = 'ts'
        PHP = 'php'
        CSS = 'css'
        HTML = 'html'
        Java = 'java'
        C = 'c'
        Cpp = 'cpp'
        CHeader = 'h'
        Shell = 'sh'
        Go = 'go'
        Dart = 'dart'

    class Data:
        YML = 'yml'
        YAML = 'yaml'
        SQL = 'sql'
        Pickle = 'pkl'
        CSV = 'csv'
        XLSX = 'xlsx'
        JSON = 'json'
        XML = 'xml'
        TSV = 'tsv'
        DOCX = 'docx'
        PPTX = 'pptx'
        PDF = 'pdf'
        TXT = 'txt'


class DataSourceMediaStorageConnection(models.Model):
    """
    DataSourceMediaStorageConnection Model:
    - Purpose: Represents a connection to a media storage system, including configurations for media categories, directory paths, and storage settings.
    - Key Fields:
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `name`: The name of the media storage connection.
        - `description`: A description of the connection.
        - `media_category`: The category of media (e.g., Image, Audio).
        - `directory_full_path`: The full directory path for storing media files.
        - `directory_schema`: JSON representation of the directory structure.
        - `interpretation_temperature`, `interpretation_maximum_tokens`: Parameters for interpreting media content.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to ensure the directory path is set if not provided.
        - `delete()`: Overridden to remove the associated directory from storage, with support for AWS S3.
    """

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    media_category = models.CharField(max_length=20, choices=MEDIA_CATEGORIES)

    directory_full_path = models.CharField(max_length=255, blank=True, null=True)
    directory_schema = models.TextField(blank=True, null=True)

    interpretation_temperature = models.FloatField(default=0.25)
    interpretation_maximum_tokens = models.IntegerField(default=2048)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + slugify(self.directory_full_path) + ' - ' + self.created_at.strftime(
            '%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Data Source Media Storage Connection'
        verbose_name_plural = 'Data Source Media Storage Connections'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assistant', 'name']),
            models.Index(fields=['assistant', 'media_category']),
            models.Index(fields=['assistant', 'directory_full_path']),
            models.Index(fields=['assistant', 'created_at']),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.directory_full_path:
            base_dir = self.assistant.storages_base_directory
            dir_suffix = self.media_category
            full_path = os.path.join(base_dir, dir_suffix)
            self.directory_full_path = full_path
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # Remove the directory
        if self.directory_full_path and os.path.exists(self.directory_full_path):
            boto3_client = boto3.client('s3')
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            s3_path = self.directory_full_path.split(MEDIA_URL)[1]
            s3_path = s3_path.replace('/', '')
            s3_path = f"{s3_path}/"
            try:
                boto3_client.delete_object(Bucket=bucket_name, Key=s3_path)
            except Exception as e:
                print(f"[DataSourceMediaStorageConnection.delete] Error occurred while deleting the directory: {str(e)}")
        super().delete(using, keep_parents)


class DataSourceMediaStorageItem(models.Model):
    """
    DataSourceMediaStorageItem Model:
    - Purpose: Represents an individual media file within a media storage connection, including metadata like file name, size, and type.
    - Key Fields:
        - `storage_base`: ForeignKey linking to the `DataSourceMediaStorageConnection` model.
        - `media_file_name`: The name of the media file.
        - `description`: A description of the media file.
        - `media_file_size`: The size of the media file.
        - `media_file_type`: The type of the media file (e.g., JPEG, MP4).
        - `full_file_path`: The full path to the media file in storage.
        - `file_bytes`: BinaryField for storing the file's content temporarily before uploading.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to slugify the file name, validate the file type, generate a unique file path, and trigger asynchronous file upload.
    """

    storage_base = models.ForeignKey('datasource_media_storages.DataSourceMediaStorageConnection',
                                     on_delete=models.CASCADE, related_name='items')

    media_file_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_file_size = models.BigIntegerField(null=True, blank=True)
    media_file_type = models.CharField(max_length=10, choices=MEDIA_FILE_TYPES)

    full_file_path = models.CharField(max_length=1000, blank=True, null=True)
    file_bytes = models.BinaryField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.media_file_name + ' - ' + self.media_file_type + ' - ' + self.created_at.strftime(
            '%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Data Source Media Storage Item'
        verbose_name_plural = 'Data Source Media Storage Items'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['storage_base', 'media_file_name']),
            models.Index(fields=['storage_base', 'media_file_type']),
            models.Index(fields=['storage_base', 'media_file_size']),
            models.Index(fields=['storage_base', 'full_file_path']),
            models.Index(fields=['storage_base', 'description']),
            models.Index(fields=['storage_base', 'created_at']),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.media_file_name = slugify(self.media_file_name)
        file_type = self.media_file_type

        if file_type not in [ft[0] for ft in MEDIA_FILE_TYPES]:
            print(f"[DataSourceMediaStorageItem.save] Invalid file format: {file_type}, skipping file...")
            return False

        if not self.full_file_path:
            base_dir = self.storage_base.directory_full_path
            file_name = self.media_file_name
            unique_suffix = str(random.randint(1_000_000, 9_999_999))
            relative_path = f"{base_dir.split(MEDIA_URL)[1]}/{file_name.split('.')[0]}_{unique_suffix}.{file_type}"
            self.full_file_path = f"{MEDIA_URL}{relative_path}"

            # Upload the file to the storage asynchronously
            upload_file_to_storage.delay(file_bytes=self.file_bytes, full_path=relative_path,
                                         media_category=self.storage_base.media_category)

        self.file_bytes = None
        super().save(force_insert, force_update, using, update_fields)

