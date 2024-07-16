import weaviate
from weaviate.config import AdditionalConfig, Timeout

from apps._services.knowledge_base.document.helpers.class_creator import create_chat_history_classes_helper
from apps._services.knowledge_base.document.helpers.class_deleter import delete_chat_history_class_helper
from apps._services.knowledge_base.document.helpers.document_deleter import delete_chat_history_document_helper
from apps.datasource_knowledge_base.tasks import index_memory_helper, embed_memory_data, embed_memory_chunks
from config.settings import WEAVIATE_CLUSTER_URL, WEAVIATE_API_KEY, WEAVIATE_SINGLE_TIME_MEMORY_RETRIEVAL_LIMIT
import weaviate.classes as wvc


class MemoryExecutor:

    def __init__(self, connection):
        self.connection_object = connection
        self.client = None

    def connect_c(self):
        try:
            c = weaviate.connect_to_weaviate_cloud(
                cluster_url=WEAVIATE_CLUSTER_URL,
                auth_credentials=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
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

    ##################################################

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

    def create_chat_history_classes(self):
        _ = self.connect_c()
        output = create_chat_history_classes_helper(executor=self)
        self.close_c()
        return output

    def delete_chat_history_classes(self, class_name: str):
        _ = self.connect_c()
        output = delete_chat_history_class_helper(executor=self, class_name=class_name)
        self.close_c()
        return output

    def delete_chat_history_document(self, class_name: str, document_uuid: str):
        _ = self.connect_c()
        output = delete_chat_history_document_helper(
            executor=self,
            class_name=class_name,
            document_uuid=document_uuid
        )
        self.close_c()
        return output

    ##################################################

    def index_memory(self, connection_id: int, assistant_id: int, chat_id: int, message_text: str):
        ##################################################
        _ = self.connect_c()
        index_memory_helper.delay(
            connection_id=connection_id,
            assistant_id=assistant_id,
            chat_id=chat_id,
            message_text=message_text
        )
        self.close_c()
        return

    def embed_memory(self, number_of_chunks: int):
        executor_params = {
            "client": {
                "host_url": WEAVIATE_CLUSTER_URL,
                "api_key": WEAVIATE_API_KEY
            },
            "connection_id": self.connection_object.id
        }
        print(f"[Memory Embedder]: Prepare to embed the memory:...")
        doc_id, doc_uuid, error = embed_memory_data(executor_params=executor_params,
                                                    number_of_chunks=number_of_chunks)
        print(f"[Document Embedder]: Embedded the document:...")
        return doc_id, doc_uuid, error

    def embed_memory_chunks(self, chunks: list, memory_id: int, memory_uuid: str):
        print(f"[Memory Chunk Embedder]: Prepare to embed the memory chunks: {memory_id}")
        executor_params = {
            "client": {
                "host_url": WEAVIATE_CLUSTER_URL,
                "api_key": WEAVIATE_API_KEY
            },
            "connection_id": self.connection_object.id
        }
        errors = embed_memory_chunks(executor_params=executor_params, chunks=chunks,
                                     memory_id=memory_id, memory_uuid=memory_uuid)
        print(f"[Document Chunk Embedder]: Embedded the memory chunks: {memory_id}")
        return errors

    def search_hybrid(self, query: str, alpha: float):
        search_memory_class_name = f"{self.connection_object.class_name}Chunks"
        client = self.connect_c()
        memories_collection = client.collections.get(search_memory_class_name)
        response = memories_collection.query.hybrid(
            query_properties=["chunk_content"],
            query=query,
            alpha=float(alpha),
            limit=int(WEAVIATE_SINGLE_TIME_MEMORY_RETRIEVAL_LIMIT)
        )
        # clean the response
        cleaned_memories = []
        for o in response.objects:
            cleaned_object = {}
            if not o.properties:
                continue
            for k, v in o.properties.items():
                if k in ["chunk_content", "chunk_number", "created_at"]:
                    cleaned_object[k] = v
            cleaned_memories.append(cleaned_object)
        return cleaned_memories
