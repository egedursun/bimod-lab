

import weaviate
import weaviate.classes as wvc
from weaviate.config import AdditionalConfig, Timeout

from apps._services.code_repository.helpers.class_creator import create_classes_helper
from apps._services.code_repository.helpers.class_deleter import delete_code_repository_class_helper
from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.datasource_code_repository.tasks import index_repository_helper

TASK_PROCESSING_TIMEOUT_SECONDS = (60 * 60)  # 60 minutes for all the tasks for a pipeline to complete


class WeaviateExecutor:

    def __init__(self, connection):
        self.connection_object = connection
        self.client = None

    def connect_c(self):
        try:
            c = weaviate.connect_to_weaviate_cloud(
                cluster_url=self.connection_object.host_url,
                auth_credentials=weaviate.auth.AuthApiKey(api_key=self.connection_object.provider_api_key),
                headers={
                    "X-OpenAI-Api-Key": self.connection_object.vectorizer_api_key
                },
                additional_config=AdditionalConfig(
                    timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
                )
            )
            print(f"[WeaviateExecutor.connect_c] Connected to Weaviate successfully.")
            self.client = c
        except Exception as e:
            return self.client
        return self.client

    def close_c(self):
        try:
            print(f"[WeaviateExecutor.close_c] Closing the Weaviate connection...")
            self.client.close()
        except Exception as e:
            pass
        return

    def retrieve_schema(self):
        try:
            c = self.connect_c()
            # retrieve the schema for weaviate
            schema = c.collections.list_all()
            print(f"[WeaviateExecutor.retrieve_schema] Retrieved the Weaviate schema successfully.")
            self.close_c()
        except Exception as e:
            print(f"Error retrieving Code Repository Weaviate schema: {e}")
            return None
        return schema

    @staticmethod
    def decode_vectorizer(vectorizer_name):
        from apps.assistants.models import VectorizerNames

        ##################################################
        # OPENAI VECTORIZER
        if vectorizer_name == VectorizerNames.TEXT2VEC_OPENAI:
            print(f"[WeaviateExecutor.decode_vectorizer] OpenAI vectorizer selected.")
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################
        # DEFAULT VECTORIZER
        else:
            print(f"[WeaviateExecutor.decode_vectorizer] Default vectorizer selected: text2vec-openai.")
            # Return the default vectorizer (text2vec-openai)
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################

    def create_weaviate_classes(self):
        _ = self.connect_c()
        output = create_classes_helper(executor=self)
        print(f"[WeaviateExecutor.create_weaviate_classes] Created the Weaviate classes successfully.")
        self.close_c()
        return output

    def delete_weaviate_classes(self, class_name: str):
        _ = self.connect_c()
        output = delete_code_repository_class_helper(executor=self, class_name=class_name)
        print(f"[WeaviateExecutor.delete_weaviate_classes] Deleted the Weaviate classes successfully.")
        self.close_c()
        return output

    def index_repository(self, document_paths: list | str):
        ##################################################
        _ = self.connect_c()
        index_repository_helper.delay(connection_id=self.connection_object.id, document_paths=document_paths)
        print(f"[WeaviateExecutor.index_repository] Indexing the repository...")
        self.close_c()
        return

    def search_hybrid(self, query: str, alpha: float):
        search_knowledge_base_class_name = f"{self.connection_object.class_name}Chunks"
        print(f"[WeaviateExecutor.search_hybrid] Searching the Weaviate hybrid...")
        client = self.connect_c()
        documents_collection = client.collections.get(search_knowledge_base_class_name)
        response = documents_collection.query.hybrid(
            query_properties=["chunk_document_file_name", "chunk_content"],
            query=query,
            alpha=float(alpha),
            limit=int(self.connection_object.search_instance_retrieval_limit)
        )
        print(f"[WeaviateExecutor.search_hybrid] Retrieved the Weaviate hybrid search response successfully.")
        # clean the response
        cleaned_documents = []
        for o in response.objects:
            cleaned_object = {}
            if not o.properties:
                continue
            for k, v in o.properties.items():
                if k in ["chunk_document_file_name", "chunk_content", "chunk_number", "created_at"]:
                    cleaned_object[k] = v
            cleaned_documents.append(cleaned_object)
        print(f"[WeaviateExecutor.search_hybrid] Cleaned the Weaviate hybrid search response successfully.")
        transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine="cl100k_base",
            llm_cost=ToolCostsMap.CodeRepositoryExecutor.COST,
            transaction_type="system",
            transaction_source=TransactionSourcesNames.CODE_REPOSITORY_SEARCH,
            is_tool_cost=True
        )
        transaction.save()
        print(f"[WeaviateExecutor.search_hybrid] Transaction saved successfully.")
        return cleaned_documents
