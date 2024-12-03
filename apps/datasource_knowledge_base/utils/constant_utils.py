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

INTRA_MEMORY_INITIAL_CHUNK_SIZE = 1000
INTRA_MEMORY_INITIAL_CHUNK_OVERLAP = 200

VECTORSTORE_SYSTEMS = [
    ('weaviate', 'Weaviate'),
]

EMBEDDING_VECTORIZER_MODELS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


class VectorStoreSystemsNames:
    WEAVIATE = 'weaviate'


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


DOCUMENT_UPLOAD_STATUS = [
    ('staged', 'Staged'),
    ('uploaded', 'Uploaded'),
    ('loaded', 'Loaded'),
    ('chunked', 'Chunked'),
    ('embedded_document', 'Embedded Document'),
    ('saved_document', 'Saved Document'),
    ('processed_document', 'Processed Document'),
    ('embedded_chunks', 'Embedded Chunks'),
    ('saved_chunks', 'Saved Chunks'),
    ('processed_chunks', 'Processed Chunks'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('partially_failed', 'Partially Failed')
]


class VectorStoreDocProcessingStatusNames:
    STAGED = 'staged'
    UPLOADED = 'uploaded'
    LOADED = 'loaded'
    CHUNKED = 'chunked'
    EMBEDDED_DOCUMENT = 'embedded_document'
    SAVED_DOCUMENT = 'saved_document'
    PROCESSED_DOCUMENT = 'processed_document'
    EMBEDDED_CHUNKS = 'embedded_chunks'
    SAVED_CHUNKS = 'saved_chunks'
    PROCESSED_CHUNKS = 'processed_chunks'
    COMPLETED = 'completed'
    FAILED = 'failed'
    PARTIALLY_FAILED = 'partially_failed'


INTRA_MEMORY_ADMIN_LIST = [
    'class_name',
    'vectorizer',
    'vectorizer_api_key',
    'created_at',
    'updated_at'
]
INTRA_MEMORY_ADMIN_FILTER = [
    'class_name',
    'vectorizer'
]
INTRA_MEMORY_ADMIN_SEARCH = [
    'class_name',
    'vectorizer'
]

INTRA_MEMORY_MEMORY_ADMIN_LIST = [
    "knowledge_base_memory_uuid",
    "knowledge_base_memory_uuid",
    "created_at",
    "updated_at"
]
INTRA_MEMORY_MEMORY_ADMIN_FILTER = [
    "knowledge_base_memory_uuid",
    "knowledge_base_memory_uuid",
    "created_at",
    "updated_at"
]
INTRA_MEMORY_MEMORY_ADMIN_SEARCH = [
    "knowledge_base_memory_uuid",
    "knowledge_base_memory_uuid",
    "created_at",
    "updated_at"
]

INTRA_MEMORY_MEMORY_CHUNK_ADMIN_LIST = [
    "chunk_number",
    "chunk_content",
    "knowledge_base_memory_uuid",
    "chunk_uuid",
    "created_at"
]
INTRA_MEMORY_MEMORY_CHUNK_ADMIN_FILTER = [
    "chunk_number",
    "chunk_content",
    "knowledge_base_memory_uuid",
    "chunk_uuid"
]
INTRA_MEMORY_MEMORY_CHUNK_ADMIN_SEARCH = [
    "chunk_number",
    "chunk_content",
    "knowledge_base_memory_uuid",
    "chunk_uuid",
    "created_at"
]

DOCUMENT_ADMIN_LIST = [
    'knowledge_base',
    'document_type',
    'document_file_name',
    'document_description',
    'document_metadata',
    'document_uri',
    'created_at',
    'updated_at'
]
DOCUMENT_ADMIN_FILTER = [
    'knowledge_base',
    'document_type',
    'document_file_name',
    'document_description',
    'document_metadata',
    'document_uri',
    'created_at',
    'updated_at'
]
DOCUMENT_ADMIN_SEARCH = [
    'knowledge_base',
    'document_type',
    'document_file_name',
    'document_description',
    'document_metadata',
    'document_uri',
    'created_at',
    'updated_at'
]

DOCUMENT_CHUNK_ADMIN_LIST = [
    'knowledge_base',
    'document',
    'chunk_document_type',
    'chunk_document_uri',
    'knowledge_base_uuid',
    'document_uuid',
    'created_at'
]
DOCUMENT_CHUNK_ADMIN_FILTER = [
    'document',
    'chunk_document_type',
    'knowledge_base_uuid',
    'document_uuid',
    'created_at'
]
DOCUMENT_CHUNK_ADMIN_SEARCH = [
    'document',
    'chunk_document_type',
    'chunk_content',
    'chunk_metadata',
    'chunk_document_uri',
    'knowledge_base_uuid',
    'created_at'
]

DOCUMENT_PROCESSING_LOG_ADMIN_LIST = [
    'document_full_uri',
    'log_message',
    'created_at'
]
DOCUMENT_PROCESSING_LOG_ADMIN_FILTER = [
    'document_full_uri',
    'log_message',
    'created_at'
]
DOCUMENT_PROCESSING_LOG_ADMIN_SEARCH = [
    'document_full_uri',
    'log_message'
]

DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_LIST = [
    'provider',
    'host_url',
    'assistant',
    'name',
    'class_name',
    'vectorizer',
    'created_at',
    'updated_at'
]
DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_FILTER = [
    'provider',
    'host_url',
    'assistant',
    'name',
    'class_name',
    'vectorizer',
    'created_at',
    'updated_at'
]
DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_SEARCH = [
    'provider',
    'host_url',
    'assistant',
    'name',
    'class_name',
    'description',
    'vectorizer',
    'created_at',
    'updated_at'
]
