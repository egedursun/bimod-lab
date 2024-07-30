

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
            self.client = c
        except Exception as e:
            return self.client
        return self.client

    def close_c(self):
        try:
            self.client.close()
        except Exception as e:
            pass
        return

    def retrieve_schema(self):
        try:
            c = self.connect_c()
            # retrieve the schema for weaviate
            schema = c.collections.list_all()
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
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################
        # DEFAULT VECTORIZER
        else:
            # Return the default vectorizer (text2vec-openai)
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################

    def create_weaviate_classes(self):
        _ = self.connect_c()
        output = create_classes_helper(executor=self)
        self.close_c()
        return output

    def delete_weaviate_classes(self, class_name: str):
        _ = self.connect_c()
        output = delete_code_repository_class_helper(executor=self, class_name=class_name)
        self.close_c()
        return output

    def index_repository(self, document_paths: list | str):
        ##################################################
        _ = self.connect_c()
        index_repository_helper.delay(connection_id=self.connection_object.id, document_paths=document_paths)
        self.close_c()
        return

    def repository_loader(self):
        # TODO:
        #    i. Download the repository with git clone
        #    ii. Save the downloaded files to a temporary folder
        #    iii. Get the paths of the files
        #    iv. Return the paths
        # clone the repository
        pass

    def document_chunker(self, file_path):
        # TODO:
        #   i. Split the document into different chunks
        #   ii. Return the chunks
        pass

    def embed_repository(self, document: dict, path: str, number_of_chunks: int = 0):
        # TODO:
        #   i. Embed the general repository data to Weaviate
        #   ii. Return the document id and uuid
        executor_params = {
            "client": {
                "host_url": self.connection_object.host_url,
                "api_key": self.connection_object.provider_api_key
            },
            "connection_id": self.connection_object.id
        }
        print(f"[Document Embedder]: Prepare to embed the repository:...")
        doc_id, doc_uuid, error = embed_repository_data(executor_params=executor_params, document=document, path=path,
                                                      number_of_chunks=number_of_chunks)
        print(f"[Document Embedder]: Embedded the repository:...")
        return doc_id, doc_uuid, error

    def embed_repository_chunks(self, chunks: list, path: str, document_id: int, document_uuid: str):
        # TODO:
        #   i. Embed the repository chunks to Weaviate
        #   ii. Return the errors
        print(f"[Repository Chunk Embedder]: Prepare to embed the repository chunks: {document_id}")
        executor_params = {
            "client": {
                "host_url": self.connection_object.host_url,
                "api_key": self.connection_object.provider_api_key
            },
            "connection_id": self.connection_object.id
        }
        errors = embed_repository_chunks(executor_params=executor_params, chunks=chunks, path=path,
                                       document_id=document_id, document_uuid=document_uuid)
        print(f"[Repository Chunk Embedder]: Embedded the repository chunks: {document_id}")
        return errors

    def search_hybrid(self, query: str, alpha: float):
        search_knowledge_base_class_name = f"{self.connection_object.class_name}Chunks"
        client = self.connect_c()
        documents_collection = client.collections.get(search_knowledge_base_class_name)
        response = documents_collection.query.hybrid(
            query_properties=["chunk_document_file_name", "chunk_content"],
            query=query,
            alpha=float(alpha),
            limit=int(self.connection_object.search_instance_retrieval_limit)
        )
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
        return cleaned_documents
