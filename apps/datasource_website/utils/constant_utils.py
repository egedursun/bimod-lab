#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-12-07 19:10:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:10:55
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


class OpenAIEmbeddingModels:
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_V2 = "text-embedding-ada-002"


OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS = 3072

VECTOR_INDEX_PATH_WEBSITE_ITEMS = os.path.join(
    BASE_DIR,
    'vectors',
    'website_vectors',
    'website_indexes'
)

WEBSITE_CRAWLING_METHODOLOGY_CHOICES = [
    ('text_content', 'Text Content'),
    ('html_content', 'HTML Content'),
]


class WebsiteIndexingMethodologyChoicesNames:
    TEXT_CONTENT = 'text_content'
    HTML_CONTENT = 'html_content'

    @staticmethod
    def as_list():
        return [
            WebsiteIndexingMethodologyChoicesNames.TEXT_CONTENT,
            WebsiteIndexingMethodologyChoicesNames.HTML_CONTENT
        ]


DATASOURCE_WEBSITE_STORAGE_ITEM_ADMIN_LIST = (
    'website_url',
    'crawling_methodology',
    'n_chunks',
    'created_at',
    'updated_at',
)
DATASOURCE_WEBSITE_STORAGE_ITEM_ADMIN_FILTER = (
    'crawling_methodology',
    'created_at',
    'updated_at',
)
DATASOURCE_WEBSITE_STORAGE_ITEM_ADMIN_SEARCH = (
    'website_url',
)

DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_LIST = (
    'website_item',
    'raw_data_hash',
    'created_at',
    'updated_at'
)
DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_FILTER = (
    'created_at',
    'updated_at'
)
DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_SEARCH = (
    'website_item__website_url',
    'raw_data_hash'
)

DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_LIST = (
    'id',
    'assistant',
    'name',
    'vectorizer',
    'embedding_chunk_size',
    'embedding_chunk_overlap',
    'search_instance_retrieval_limit',
    'maximum_pages_to_index',
    'created_at',
    'updated_at',
)
DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_FILTER = (
    'assistant',
    'vectorizer',
    'embedding_chunk_size',
    'embedding_chunk_overlap',
    'search_instance_retrieval_limit',
    'maximum_pages_to_index',
    'created_at',
    'updated_at',
)
DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_SEARCH = (
    'assistant',
    'name',
    'vectorizer',
    'embedding_chunk_size',
    'embedding_chunk_overlap',
    'search_instance_retrieval_limit',
    'maximum_pages_to_index',
    'created_at',
    'updated_at',
)
