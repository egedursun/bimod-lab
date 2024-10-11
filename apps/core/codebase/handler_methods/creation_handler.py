#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: class_creator.py
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

from apps.core.codebase.utils import REPOSITORY_WEAVIATE_FIELDS_CONFIG, REPOSITORY_CHUNK_WEAVIATE_FIELDS_CONFIG
from apps.core.codebase.utils import DEFAULT_GENERATIVE_SEARCH_MODEL


def create_classes_helper(executor):
    output = {"status": True, "error": ""}
    conn = executor.connection_object
    c = executor.connect_c()

    try:
        _ = c.collections.create(
            name=conn.class_name,
            vectorizer_config=executor.decode_vectorizer(conn.vectorizer),
            generative_config=wvc.config.Configure.Generative.openai(
                model=DEFAULT_GENERATIVE_SEARCH_MODEL, temperature=conn.assistant.llm_model.temperature,
                max_tokens=conn.assistant.llm_model.maximum_tokens), properties=REPOSITORY_WEAVIATE_FIELDS_CONFIG)
    except Exception as e:
        output["status"] = False
        output["error"] = str(e)
        return output

    try:
        _ = c.collections.create(
            name=f"{conn.class_name}Chunks",
            vectorizer_config=executor.decode_vectorizer(conn.vectorizer),
            generative_config=wvc.config.Configure.Generative.openai(
                model=DEFAULT_GENERATIVE_SEARCH_MODEL, temperature=conn.assistant.llm_model.temperature,
                max_tokens=conn.assistant.llm_model.maximum_tokens
            ),
            properties=REPOSITORY_CHUNK_WEAVIATE_FIELDS_CONFIG)
    except Exception as e:
        output["status"] = False
        output["error"] = str(e)
        return output
    return output
