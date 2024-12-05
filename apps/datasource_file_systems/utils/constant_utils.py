#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import os

from config.settings import BASE_DIR

SSH_CONNECTION_DEFAULT_BANNER_TIMEOUT = 200

DATASOURCE_FILE_SYSTEMS_OS_TYPES = [
    ('linux', 'Linux'),
    ('macos', 'MacOS'),
]


class DataSourceFileSystemsOsTypeNames:
    LINUX = 'linux'
    MACOS = 'macos'


FILE_SYSTEM_ADMIN_LIST = (
    'name',
    'os_type',
    'host_url',
    'port',
    'username',
    'is_read_only'
)

FILE_SYSTEM_ADMIN_FILTER = (
    'os_type',
    'is_read_only'
)

FILE_SYSTEM_ADMIN_SEARCH = (
    'name',
    'host_url',
    'username',
    'ssh_connection_uri'
)

DEFAULT_SEARCH_RESULTS_FILE_SYSTEM_DIRECTORY_SCHEMA = 10


class OpenAIEmbeddingModels:
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_V2 = "text-embedding-ada-002"


OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS = 3072

VECTOR_INDEX_PATH_FILE_SYSTEM_DIRECTORY_SCHEMAS = os.path.join(
    BASE_DIR,
    'vectors',
    'file_system_schema_vectors',
    'file_system_schemas'
)

FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_SIZE = 2_000
FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_OVERLAP = 1_000

FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST = (
    'file_system',
    'created_at',
    'updated_at'
)
FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER = (
    'file_system',
    'created_at',
    'updated_at'
)
FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH = (
    'file_system',
    'created_at',
    'updated_at'
)

FILE_SYSTEM_DIRECTORY_SCHEMA_MAX_CHARACTERS_LIMIT = 100_000_000_000
FILE_SYSTEM_DIRECTORY_SCHEMA_MAX_DEPTH = 1000
