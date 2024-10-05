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
#
#

import weaviate.classes as wvc


DEFAULT_GENERATIVE_SEARCH_MODEL = "gpt-4"


def create_classes_helper(executor):
    output = {"status": True, "error": ""}
    conn = executor.connection_object
    c = executor.connect_c()
    print(f"[class_creator.create_classes_helper] Creating Weaviate classes...")

    try:
        _ = c.collections.create(
            name=conn.class_name,
            vectorizer_config=executor.decode_vectorizer(
                conn.vectorizer
            ),
            generative_config=wvc.config.Configure.Generative.openai(
                model=DEFAULT_GENERATIVE_SEARCH_MODEL,
                temperature=conn.assistant.llm_model.temperature,
                max_tokens=conn.assistant.llm_model.maximum_tokens,
            ),
            properties=[
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
                ##################################################
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
        )
        print(f"[class_creator.create_classes_helper] Created Weaviate class: {conn.class_name}")
    except Exception as e:
        print(f"[class_creator.create_classes_helper] Error creating Weaviate class: {e}")
        output["status"] = False
        output["error"] = str(e)
        return output

    try:
        _ = c.collections.create(
            name=f"{conn.class_name}Chunks",
            vectorizer_config=executor.decode_vectorizer(
                conn.vectorizer
            ),
            generative_config=wvc.config.Configure.Generative.openai(
                model=DEFAULT_GENERATIVE_SEARCH_MODEL,
                temperature=conn.assistant.llm_model.temperature,
                max_tokens=conn.assistant.llm_model.maximum_tokens,
            ),
            properties=[
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
        )
        print(f"[class_creator.create_classes_helper] Created Weaviate class: {conn.class_name}Chunks")
    except Exception as e:
        print(f"Error creating Weaviate class: {e}")
        output["status"] = False
        output["error"] = str(e)
        return output
    print(f"[class_creator.create_classes_helper] Created Weaviate classes successfully.")
    return output


def create_chat_history_classes_helper(executor):
    output = {"status": True, "error": ""}
    conn = executor.connection_object
    c = executor.connect_c()
    print(f"[class_creator.create_chat_history_classes_helper] Creating Chat History Weaviate classes...")

    try:
        _ = c.collections.create(
            name=conn.class_name,
            vectorizer_config=executor.decode_vectorizer(
                conn.vectorizer
            ),
            generative_config=wvc.config.Configure.Generative.openai(
                model=DEFAULT_GENERATIVE_SEARCH_MODEL,
                temperature=conn.assistant.llm_model.temperature,
                max_tokens=conn.assistant.llm_model.maximum_tokens,
            ),
            properties=[
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
        )
        print(f"[class_creator.create_chat_history_classes_helper] Created Chat History class: {conn.class_name}")
    except Exception as e:
        print(f"Error creating Chat History class: {e}")
        output["status"] = False
        output["error"] = str(e)
        return output

    try:
        _ = c.collections.create(
            name=f"{conn.class_name}Chunks",
            vectorizer_config=executor.decode_vectorizer(
                conn.vectorizer
            ),
            generative_config=wvc.config.Configure.Generative.openai(
                model=DEFAULT_GENERATIVE_SEARCH_MODEL,
                temperature=conn.assistant.llm_model.temperature,
                max_tokens=conn.assistant.llm_model.maximum_tokens,
            ),
            properties=[
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
        ])
        print(f"[class_creator.create_chat_history_classes_helper] Created Chat History Chunks class: {conn.class_name}Chunks")
    except Exception as e:
        print(f"[class_creator.create_chat_history_classes_helper] Error creating Chat History Chunks class: {e}")
        output["status"] = False
        output["error"] = str(e)
        return output
    print(f"[class_creator.create_chat_history_classes_helper] Created Chat History Weaviate classes successfully.")
    return output
