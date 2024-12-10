#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import weaviate.classes as wvc

DEFAULT_GENERATIVE_SEARCH_MODEL = "gpt-4"

WEAVIATE_INITIALIZATION_TIMEOUT = 60
WEAVIATE_QUERY_TIMEOUT = 120
WEAVIATE_INSERT_TIMEOUT = 240

KNOWLEDGE_BASE_PROVIDERS = {
    "WEAVIATE": {
        "code": "weaviate",
        "name": "Weaviate"
    },
}

REPOSITORY_WEAVIATE_FIELDS_CONFIG = [
    wvc.config.Property(
        name="repository_file_name",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=True,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),

    wvc.config.Property(
        name="repository_description",
        data_type=wvc.config.DataType.TEXT,
        vectorize_property_name=False,
        tokenization=wvc.config.Tokenization.LOWERCASE
    ),

    wvc.config.Property(
        name="repository_metadata",
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

REPOSITORY_CHUNK_WEAVIATE_FIELDS_CONFIG = [
    wvc.config.Property(
        name="chunk_repository_file_name",
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
