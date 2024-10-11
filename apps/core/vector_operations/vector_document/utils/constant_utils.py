#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


import weaviate.classes as wvc

WEAVIATE_INITIALIZATION_TIMEOUT = 60
WEAVIATE_QUERY_TIMEOUT = 120
WEAVIATE_INSERT_TIMEOUT = 240


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


VECTOR_STORE_DOCUMENT_WEAVIATE_FIELDS_CONFIG = [
    wvc.config.Property(
        name="document_file_name",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="document_description",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=False,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="document_type",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="document_metadata",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="number_of_chunks",
        data_type=wvc.config.DataType.INT,
        vectorize_property_name=False,
    ),
    wvc.config.Property(
        name="created_at",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=False,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
]

VECTOR_STORE_DOCUMENT_CHUNK_WEAVIATE_FIELDS_CONFIG = [
    wvc.config.Property(
        name="chunk_document_file_name",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="chunk_document_type",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="chunk_number",
        data_type=wvc.config.DataType.INT,
        vectorize_property_name=False,
    ),
    wvc.config.Property(
        name="chunk_content",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="chunk_metadata",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="created_at",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=False,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
]

CONTEXT_MEMORY_OBJECT_WEAVIATE_FIELDS_CONFIG = [
    wvc.config.Property(
        name="memory_name",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
    ),
    wvc.config.Property(
        name="number_of_chunks",
        data_type=wvc.config.DataType.INT,
        vectorize_property_name=False,
    ),
    wvc.config.Property(
        name="created_at",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=False,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
]

CONTEXT_MEMORY_CHUNKS_WEAVIATE_FIELDS_CONFIG = [
    wvc.config.Property(
        name="memory_name",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=False,
    ),
    wvc.config.Property(
        name="chunk_number",
        data_type=wvc.config.DataType.INT,
        vectorize_property_name=False,
    ),
    wvc.config.Property(
        name="chunk_content",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
    wvc.config.Property(
        name="created_at",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=False,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),
]
