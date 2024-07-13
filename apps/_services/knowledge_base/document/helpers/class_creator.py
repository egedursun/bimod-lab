import weaviate.classes as wvc


DEFAULT_GENERATIVE_SEARCH_MODEL = "gpt-4-32k"


def create_classes_helper(executor):
    output = {"status": True, "error": ""}
    conn = executor.connection_object
    c = executor.client

    try:
        new_document_class = c.collections.create(
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
    except Exception as e:
        print(f"Error creating Weaviate class: {e}")
        output["status"] = False
        output["error"] = str(e)
        return output

    try:
        document_chunk_class = c.collections.create(
            name=f"{conn.class_name}Chunks",
            vectorizer_config=executor.decode_vectorizer(
                conn.vectorizer
            ),
            generative_config=wvc.config.Configure.Generative.openai(
                model="gpt-4-32k",
                temperature=conn.assistant.llm_model.temperature,
                max_tokens=conn.assistant.llm_model.maximum_tokens,
            ),
            properties=[
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
    except Exception as e:
        print(f"Error creating Weaviate class: {e}")
        output["status"] = False
        output["error"] = str(e)
        return output

    print(f"Created Weaviate classes: {new_document_class}, {document_chunk_class}")
    return output
