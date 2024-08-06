import weaviate
from weaviate.config import AdditionalConfig, Timeout

from apps._services.config.costs_map import ToolCostsMap
from apps._services.knowledge_base.document.helpers.class_creator import create_chat_history_classes_helper
from apps._services.knowledge_base.document.helpers.class_deleter import delete_chat_history_class_helper
from apps._services.knowledge_base.document.helpers.document_deleter import delete_chat_history_document_helper
from apps.datasource_knowledge_base.tasks import index_memory_helper, embed_memory_data, embed_memory_chunks
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from config.settings import WEAVIATE_CLUSTER_URL, WEAVIATE_API_KEY, WEAVIATE_SINGLE_TIME_MEMORY_RETRIEVAL_LIMIT
import weaviate.classes as wvc


WEAVIATE_INITIALIZATION_TIMEOUT = 30  # 30 seconds for the weaviate initialization
WEAVIATE_QUERY_TIMEOUT = 60  # 60 seconds for the weaviate query
WEAVIATE_INSERT_TIMEOUT = 120  # 120 seconds for the weaviate insert


class MemoryExecutor:
    def __init__(self, connection):
        self.connection_object = connection
        self.client = None

    def connect_c(self):
        try:
            c = weaviate.connect_to_weaviate_cloud(
                cluster_url=WEAVIATE_CLUSTER_URL,
                auth_credentials=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
                headers={"X-OpenAI-Api-Key": self.connection_object.vectorizer_api_key},
                additional_config=AdditionalConfig(
                    timeout=Timeout(init=WEAVIATE_INITIALIZATION_TIMEOUT,
                                    query=WEAVIATE_QUERY_TIMEOUT,
                                    insert=WEAVIATE_INSERT_TIMEOUT)
                )
            )
            print(f"[MemoryExecutor.connect_c] Connected to Weaviate successfully.")
            self.client = c
        except Exception as e:
            return self.client
        return self.client

    def close_c(self):
        try:
            self.client.close()
            print(f"[MemoryExecutor.close_c] Closed the Weaviate connection successfully.")
        except Exception as e:
            pass
        return

    ##################################################

    @staticmethod
    def decode_vectorizer(vectorizer_name):
        from apps.assistants.models import VectorizerNames
        if vectorizer_name == VectorizerNames.TEXT2VEC_OPENAI:
            print(f"[MemoryExecutor.decode_vectorizer] Using OpenAI vectorizer.")
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        else:
            print(f"[MemoryExecutor.decode_vectorizer] Using OpenAI vectorizer: text2vec_openai.")
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################

    def create_chat_history_classes(self):
        try:
            _ = self.connect_c()
            output = create_chat_history_classes_helper(executor=self)
            print(f"[MemoryExecutor.create_chat_history_classes] Created Chat History classes.")
            self.close_c()
        except Exception as e:
            print(f"[MemoryExecutor.create_chat_history_classes] Error: {str(e)}")
            return False
        return output

    def delete_chat_history_classes(self, class_name: str):
        try:
            _ = self.connect_c()
            output = delete_chat_history_class_helper(executor=self, class_name=class_name)
            print(f"[MemoryExecutor.delete_chat_history_classes] Deleted Chat History classes.")
            self.close_c()
        except Exception as e:
            print(f"[MemoryExecutor.delete_chat_history_classes] Error: {str(e)}")
            return False
        return output

    def delete_chat_history_document(self, class_name: str, document_uuid: str):
        try:
            _ = self.connect_c()
            output = delete_chat_history_document_helper(
                executor=self,
                class_name=class_name,
                document_uuid=document_uuid
            )
            print(f"[MemoryExecutor.delete_chat_history_document] Deleted Chat History document: {document_uuid}")
            self.close_c()
        except Exception as e:
            print(f"[MemoryExecutor.delete_chat_history_document] Error: {str(e)}")
            return False
        return output

    ##################################################

    def index_memory(self, connection_id: int, message_text: str):
        try:
            _ = self.connect_c()
            index_memory_helper.delay(connection_id=connection_id, message_text=message_text)
            print(f"[MemoryExecutor.index_memory] Indexed the memory.")
            self.close_c()
        except Exception as e:
            print(f"[MemoryExecutor.index_memory] Error: {str(e)}")
            return False
        return

    def embed_memory(self, number_of_chunks: int):
        executor_params = {
            "client": {"host_url": WEAVIATE_CLUSTER_URL, "api_key": WEAVIATE_API_KEY},
            "connection_id": self.connection_object.id}
        try:
            doc_id, doc_uuid, error = embed_memory_data(executor_params=executor_params,
                                                        number_of_chunks=number_of_chunks)
            print(f"[MemoryExecutor.embed_memory] Embedded the memory.")
        except Exception as e:
            print(f"[MemoryExecutor.embed_memory] Error: {str(e)}")
            return None, None, str(e)
        return doc_id, doc_uuid, error

    def embed_memory_chunks(self, chunks: list, memory_id: int, memory_uuid: str):
        executor_params = {
            "client": {"host_url": WEAVIATE_CLUSTER_URL, "api_key": WEAVIATE_API_KEY},
            "connection_id": self.connection_object.id}
        try:
            errors = embed_memory_chunks(executor_params=executor_params, chunks=chunks,
                                         memory_id=memory_id, memory_uuid=memory_uuid)
            print(f"[MemoryExecutor.embed_memory_chunks] Embedded the memory chunks.")
        except Exception as e:
            print(f"[MemoryExecutor.embed_memory_chunks] Error: {str(e)}")
            return str(e)
        return errors

    def search_hybrid(self, query: str, alpha: float):
        from apps._services.llms.openai import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
        search_memory_class_name = f"{self.connection_object.class_name}Chunks"
        client = self.connect_c()
        memories_collection = client.collections.get(search_memory_class_name)
        response = memories_collection.query.hybrid(
            query_properties=["chunk_content"],
            query=query,
            alpha=float(alpha),
            limit=int(WEAVIATE_SINGLE_TIME_MEMORY_RETRIEVAL_LIMIT)
        )
        print(f"[MemoryExecutor.search_hybrid] Search completed successfully.")
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
        print(f"[MemoryExecutor.search_hybrid] Cleaned the memories.")

        try:
            transaction = LLMTransaction(
                organization=self.connection_object.assistant.organization,
                model=self.connection_object.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection_object.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.ContextMemoryRetrieval.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.RETRIEVE_MEMORY,
                is_tool_cost=True
            )
            transaction.save()
            print(f"[MemoryExecutor.search_hybrid] Transaction saved successfully.")
        except Exception as e:
            print(f"[MemoryExecutor.search_hybrid] Error occurred while saving the transaction: {str(e)}")
            return {"success": False, "message": "Error occurred while saving the transaction.", "memories": []}
        return cleaned_memories
