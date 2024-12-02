#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#


MEDIA_MANAGER_ITEM_TYPES = (
    ('image', 'Image'),
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('compressed', 'Compressed'),
    ('code', 'Code'),
    ('data', 'Data'),
)


class MediaManagerItemCategoriesNames:
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


class MediaManagerItemFormatTypesNames:
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


class MediaManagerItemFormatTypesNamesLists:
    IMAGE = ['jpg', 'png', 'gif', 'svg', 'bmp', 'tiff']
    AUDIO = ['mp3', 'wav', 'flac', 'aac', 'ogg']
    VIDEO = ['mp4', 'avi', 'mkv', 'mov']
    COMPRESSED = ['zip', 'rar', 'tar']
    CODE = ['py', 'js', 'ts', 'php', 'css', 'html', 'java', 'c', 'cpp', 'h', 'sh', 'go', 'dart']
    DATA = ['yml', 'yaml', 'sql', 'pkl', 'csv', 'xlsx', 'json', 'xml', 'tsv', 'docx', 'pptx', 'pdf', 'txt']


FILE_TYPE_HIGHLIGHTING_DECODER = {
    "py": "python", "js": "javascript", "ts": "typescript", "php": "php", "css": "css", "html": "html",
    "java": "java", "c": "c", "cpp": "cpp", "h": "h", "sh": "shell", "go": "golang", "dart": "dart",
    "yml": "yaml", "yaml": "yaml", "sql": "sql", "pkl": "plaintext", "csv": "plaintext",
    "xlsx": "plaintext", "json": "json", "xml": "xml", "tsv": "plaintext", "docx": "plaintext",
    "pptx": "plaintext", "pdf": "plaintext", "txt": "plaintext",
}
MEDIA_MANAGER_ITEM_ADMIN_LIST_DISPLAY = ['storage_base', 'media_file_name', 'media_file_size', 'media_file_type',
                                         'full_file_path', 'created_at', 'updated_at']
MEDIA_MANAGER_ITEM_ADMIN_LIST_FILTER = ['storage_base', 'media_file_type', 'media_file_type']
MEDIA_MANAGER_ITEM_ADMIN_SEARCH_FIELDS = ['storage_base', 'media_file_name', 'full_file_path']

MEDIA_STORE_ADMIN_LIST_DISPLAY = ['assistant', 'name', 'media_category', 'directory_full_path', 'directory_schema',
                                  'created_at', 'updated_at']
MEDIA_STORE_ADMIN_LIST_FILTER = ['assistant', 'media_category']
MEDIA_STORE_ADMIN_SEARCH_FIELDS = ['assistant', 'name', 'directory_full_path']


UNIT_BYTES_THOUSAND = 1024

AI_GENERATED_DESCRIPTION_SPECIFIER = 'generated_description'
MEDIA_ITEM_VECTOR_DATA_ADMIN_LIST = (
    'media_item',
    'created_at',
    'updated_at',
)
MEDIA_ITEM_VECTOR_DATA_ADMIN_FILTER = (
    'created_at',
    'updated_at',
)
MEDIA_ITEM_VECTOR_DATA_ADMIN_SEARCH = (
    'media_item__media_file_name',
    'media_item__storage_base__name',
)
