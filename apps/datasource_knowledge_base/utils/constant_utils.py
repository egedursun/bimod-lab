#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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

INTRA_MEMORY_INITIAL_CHUNK_SIZE = 1000
INTRA_MEMORY_INITIAL_CHUNK_OVERLAP = 200

VECTOR_INDEX_PATH_KNOWLEDGE_BASE_DOCUMENTS = os.path.join(
    "vectors",
    "knowledge_base_vectors",
    "knowledge_base_indexes"
)

class OpenAIEmbeddingModels:
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_V2 = "text-embedding-ada-002"


OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS = 3072


EMBEDDING_VECTORIZER_MODELS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


UPLOAD_FILES_SUPPORTED_FORMATS = [
    ('pdf', 'PDF'),
    ('html', 'HTML'),
    ('csv', 'CSV'),
    ('docx', 'DOCX'),
    ('ipynb', 'IPYNB'),
    ('json', 'JSON'),
    ('xml', 'XML'),
    ('txt', 'TXT'),
    ('md', 'MD'),
    ('rtf', 'RTF'),
    ('odt', 'ODT'),
    ('pptx', 'POWERPOINT'),
    ('xlsx', 'XLSX')
]


class UploadFilesSupportedFormatsNames:
    PDF = 'pdf'
    HTML = 'html'
    CSV = 'csv'
    DOCX = 'docx'
    IPYNB = 'ipynb'
    JSON = 'json'
    XML = 'xml'
    TXT = 'txt'
    MD = 'md'
    RTF = 'rtf'
    ODT = 'odt'
    POWERPOINT = 'pptx'
    XLSX = 'xlsx'


INTRA_MEMORY_ADMIN_LIST = [
    'vectorizer',
    'created_at',
    'updated_at'
]
INTRA_MEMORY_ADMIN_FILTER = [
    'vectorizer'
]
INTRA_MEMORY_ADMIN_SEARCH = [
    'vectorizer'
]

INTRA_MEMORY_MEMORY_ADMIN_LIST = [
    "created_at",
    "updated_at"
]
INTRA_MEMORY_MEMORY_ADMIN_FILTER = [
    "created_at",
    "updated_at"
]
INTRA_MEMORY_MEMORY_ADMIN_SEARCH = [
    "created_at",
    "updated_at"
]

INTRA_MEMORY_MEMORY_CHUNK_ADMIN_LIST = [
    "created_at"
]
INTRA_MEMORY_MEMORY_CHUNK_ADMIN_FILTER = [
    "created_at"
]
INTRA_MEMORY_MEMORY_CHUNK_ADMIN_SEARCH = [
    "created_at"
]

DOCUMENT_ADMIN_LIST = [
    'knowledge_base',
    'document_type',
    'document_file_name',
    'document_description',
    'document_metadata',
    'created_at',
    'updated_at'
]
DOCUMENT_ADMIN_FILTER = [
    'knowledge_base',
    'document_type',
    'document_file_name',
    'document_description',
    'document_metadata',
    'created_at',
    'updated_at'
]
DOCUMENT_ADMIN_SEARCH = [
    'knowledge_base',
    'document_type',
    'document_file_name',
    'document_description',
    'document_metadata',
    'created_at',
    'updated_at'
]

DOCUMENT_CHUNK_ADMIN_LIST = [
    'knowledge_base_document',
    'chunk_document_type',
    'created_at'
]
DOCUMENT_CHUNK_ADMIN_FILTER = [
    'knowledge_base_document',
    'chunk_document_type',
    'created_at'
]
DOCUMENT_CHUNK_ADMIN_SEARCH = [
    'knowledge_base_document',
    'created_at'
]

DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_LIST = [
    'assistant',
    'name',
    'vectorizer',
    'created_at',
    'updated_at'
]
DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_FILTER = [
    'assistant',
    'name',
    'vectorizer',
    'created_at',
    'updated_at'
]
DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_SEARCH = [
    'assistant',
    'name',
    'description',
    'vectorizer',
    'created_at',
    'updated_at'
]
