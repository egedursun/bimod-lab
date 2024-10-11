#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: memory_executor.py
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

import weaviate
from weaviate.config import AdditionalConfig, Timeout

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.vector_operations.vector_document.handler_methods.creation_handler import create_intra_context_history_classes_helper
from apps.core.vector_operations.vector_document.handler_methods.removal_handler_context_memory import delete_intra_context_history_class_helper
from apps.core.vector_operations.vector_document.handler_methods.removal_handler_document import delete_chat_history_document_helper
from apps.core.vector_operations.intra_context_memory.utils import WEAVIATE_INITIALIZATION_TIMEOUT, WEAVIATE_QUERY_TIMEOUT, \
    WEAVIATE_INSERT_TIMEOUT
from apps.datasource_knowledge_base.tasks import index_memory_helper, embed_memory_data, embed_memory_chunks
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from config.settings import WEAVIATE_CLUSTER_URL, WEAVIATE_API_KEY, WEAVIATE_SINGLE_TIME_MEMORY_RETRIEVAL_LIMIT
import weaviate.classes as wvc


class IntraContextMemoryExecutor:
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
                                    insert=WEAVIATE_INSERT_TIMEOUT)))
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

    @staticmethod
    def decode_vectorizer(vectorizer_name):
        from apps.assistants.utils import EmbeddingManagersNames
        if vectorizer_name == EmbeddingManagersNames.TEXT2VEC_OPENAI:
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        else:
            return wvc.config.Configure.Vectorizer.text2vec_openai()

    def create_chat_history_classes(self):
        try:
            _ = self.connect_c()
            output = create_intra_context_history_classes_helper(executor=self)
            self.close_c()
        except Exception as e:
            return False
        return output

    def delete_chat_history_classes(self, class_name: str):
        try:
            _ = self.connect_c()
            output = delete_intra_context_history_class_helper(executor=self, class_name=class_name)
            self.close_c()
        except Exception as e:
            return False
        return output

    def delete_chat_history_document(self, class_name: str, document_uuid: str):
        try:
            _ = self.connect_c()
            data = delete_chat_history_document_helper(executor=self, class_name=class_name, document_uuid=document_uuid)
            self.close_c()
        except Exception as e:
            return False
        return data

    def index_memory(self, connection_id: int, message_text: str):
        try:
            _ = self.connect_c()
            index_memory_helper.delay(connection_id=connection_id, message_text=message_text)
            self.close_c()
        except Exception as e:
            return False
        return

    def embed_memory(self, number_of_chunks: int):
        executor_params = {
            "client": {
                "host_url": WEAVIATE_CLUSTER_URL,
                "api_key": WEAVIATE_API_KEY
            },
            "connection_id": self.connection_object.id
        }
        try:
            doc_id, doc_uuid, error = embed_memory_data(executor_params=executor_params,
                                                        number_of_chunks=number_of_chunks)
        except Exception as e:
            return None, None, str(e)
        return doc_id, doc_uuid, error

    def embed_memory_chunks(self, chunks: list, memory_id: int, memory_uuid: str):
        executor_params = {
            "client": {
                "host_url": WEAVIATE_CLUSTER_URL,
                "api_key": WEAVIATE_API_KEY
            },
            "connection_id": self.connection_object.id
        }
        try:
            errors = embed_memory_chunks(executor_params=executor_params, chunks=chunks,
                                         memory_id=memory_id, memory_uuid=memory_uuid)
        except Exception as e:
            return str(e)
        return errors

    def search_hybrid(self, query: str, alpha: float):
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        class_name = f"{self.connection_object.class_name}Chunks"
        c = self.connect_c()
        collection = c.collections.get(class_name)
        vector_store_response = collection.query.hybrid(
            query_properties=["chunk_content"],
            query=query,
            alpha=float(alpha),
            limit=int(WEAVIATE_SINGLE_TIME_MEMORY_RETRIEVAL_LIMIT)
        )
        memories = []
        for o in vector_store_response.objects:
            instance_obj = {}
            if not o.properties:
                continue
            for k, v in o.properties.items():
                if k in ["chunk_content", "chunk_number", "created_at"]:
                    instance_obj[k] = v
            memories.append(instance_obj)

        try:
            tx = LLMTransaction(
                organization=self.connection_object.assistant.organization,
                model=self.connection_object.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection_object.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.ContextMemoryRetrieval.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.RETRIEVE_MEMORY,
                is_tool_cost=True
            )
            tx.save()
        except Exception as e:
            return {"success": False, "message": "Error occurred while saving the transaction.", "memories": []}
        return memories
