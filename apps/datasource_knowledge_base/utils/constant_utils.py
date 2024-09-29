#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: constant_utils.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:45:15
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

MEMORY_DEFAULT_CHUNK_SIZE = 1000
MEMORY_DEFAULT_CHUNK_OVERLAP = 200

KNOWLEDGE_BASE_SYSTEMS = [
    ('weaviate', 'Weaviate'),
]

VECTORIZERS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


class KnowledgeBaseSystemNames:
    WEAVIATE = 'weaviate'


SUPPORTED_DOCUMENT_TYPES = [
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


class SupportedDocumentTypesNames:
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


class DocumentUploadStatusNames:
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
