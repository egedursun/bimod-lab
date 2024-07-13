import weaviate
import weaviate.classes as wvc

from apps.assistants.models import VectorizerNames


class WeaviateExecutor:

    def __init__(self, connection):
        self.connection_object = connection
        self.client = None
        host_url = self.connection_object.host_url
        weaviate_api_key = self.connection_object.provider_api_key
        try:
            c = weaviate.connect_to_weaviate_cloud(
                cluster_url=host_url,
                auth_credentials=weaviate.auth.AuthApiKey(api_key=weaviate_api_key)
            )
            self.client = c
        except Exception as e:
            print(f"Error connecting to Weaviate: {e}")

    def close_connection(self):
        try:
            self.client.close()
        except Exception as e:
            pass

    def retrieve_schema(self):
        c = self.client

        try:
            # retrieve the schema for weaviate
            schema = c.collections.list_all()
        except Exception as e:
            print(f"Error retrieving Weaviate schema: {e}")
            return None

        self.close_connection()
        return schema

    @staticmethod
    def decode_vectorizer(vectorizer_name):
        ##################################################
        # OPENAI VECTORIZER
        if vectorizer_name == VectorizerNames.TEXT2VEC_OPENAI:
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################
        # DEFAULT VECTORIZER
        else:
            # Return the default vectorizer (text2vec-openai)
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################

    def create_weaviate_classes(self):
        output = {"status": True, "error": ""}
        conn = self.connection_object
        c = self.client

        try:
            new_document_class = c.collections.create(
                name=conn.class_name,
                vectorizer_config=self.decode_vectorizer(
                    conn.vectorizer
                ),
                generative_config=wvc.config.Configure.Generative.openai(
                    model="gpt-4-32k",
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
                vectorizer_config=self.decode_vectorizer(
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
        self.close_connection()
        return output


