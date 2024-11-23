#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: knowledge_base_executor.py
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
import logging

import weaviate
import weaviate.classes as wvc
from weaviate.config import AdditionalConfig, Timeout

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.vector_operations.vector_document.handler_methods.creation_handler import \
    create_weaviate_classes_handler
from apps.core.vector_operations.vector_document.handler_methods.removal_handler_context_memory import \
    delete_weaviate_class_handler
from apps.core.vector_operations.vector_document.handler_methods.removal_handler_document import delete_document_helper
from apps.core.vector_operations.vector_document.utils import WEAVIATE_INITIALIZATION_TIMEOUT, WEAVIATE_QUERY_TIMEOUT, \
    WEAVIATE_INSERT_TIMEOUT
from apps.datasource_knowledge_base.tasks import split_document_into_chunks, embed_document_data, \
    embed_document_chunks, index_document_helper
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames

logger = logging.getLogger(__name__)


class WeaviateExecutor:

    def __init__(self, connection):
        self.connection_object = connection
        self.client = None

    def connect_c(self):
        try:
            c = weaviate.connect_to_weaviate_cloud(
                cluster_url=self.connection_object.host_url,
                auth_credentials=weaviate.auth.AuthApiKey(
                    api_key=self.connection_object.provider_api_key
                ),
                headers={
                    "X-OpenAI-Api-Key": self.connection_object.vectorizer_api_key
                },
                additional_config=AdditionalConfig(
                    timeout=Timeout(
                        init=WEAVIATE_INITIALIZATION_TIMEOUT,
                        query=WEAVIATE_QUERY_TIMEOUT,
                        insert=WEAVIATE_INSERT_TIMEOUT)
                )
            )
            self.client = c
            logger.info(f"Connected to Weaviate successfully.")

        except Exception as e:
            logger.error(f"Error occurred while connecting to Weaviate: {e}")
            return self.client

        return self.client

    def close_c(self):
        try:
            self.client.close()
            logger.info(f"Closed the Weaviate connection successfully.")

        except Exception as e:
            logger.error(f"Error occurred while closing the Weaviate connection: {e}")
            pass

        return

    def retrieve_schema(self):

        try:
            c = self.connect_c()
            schema = c.collections.list_all()
            self.close_c()
            logger.info(f"Retrieved schema: {schema}")

        except Exception as e:
            logger.error(f"Error occurred while retrieving schema: {e}")
            return None

        return schema

    @staticmethod
    def decode_vectorizer(vectorizer_name):

        from apps.assistants.utils import EmbeddingManagersNames

        if vectorizer_name == EmbeddingManagersNames.TEXT2VEC_OPENAI:
            logger.info(f"Vectorizer is set to: {vectorizer_name}")
            return wvc.config.Configure.Vectorizer.text2vec_openai()

        else:
            logger.info(f"Vectorizer is set to: {vectorizer_name}")
            return wvc.config.Configure.Vectorizer.text2vec_openai()

    def create_weaviate_classes(self):

        try:
            _ = self.connect_c()
            data = create_weaviate_classes_handler(
                executor=self
            )

            logger.info(f"Created Weaviate classes successfully.")
            self.close_c()

        except Exception as e:
            logger.error(f"Error occurred while creating Weaviate classes: {e}")
            return None

        return data

    def delete_weaviate_classes(self, class_name: str):

        try:
            _ = self.connect_c()
            data = delete_weaviate_class_handler(
                executor=self,
                class_name=class_name
            )
            self.close_c()

            logger.info(f"Deleted Weaviate classes successfully.")

        except Exception as e:
            logger.error(f"Error occurred while deleting Weaviate classes: {e}")
            return None

        return data

    def delete_weaviate_document(
        self,
        class_name: str,
        document_uuid: str
    ):

        try:
            _ = self.connect_c()
            logger.info(f"Deleting document: {document_uuid}")

            data = delete_document_helper(
                executor=self,
                class_name=class_name,
                document_uuid=document_uuid
            )

            self.close_c()

        except Exception as e:
            logger.error(f"Error occurred while deleting document: {e}")
            return None

        return data

    def index_documents(
        self,
        document_paths: list | str
    ):

        try:
            _ = self.connect_c()
            logger.info(f"Indexing documents: {document_paths}")

            index_document_helper.delay(
                connection_id=self.connection_object.id,
                document_paths=document_paths
            )

            self.close_c()

        except Exception as e:
            logger.error(f"Error occurred while indexing documents: {e}")
            return None

        return

    def chunk_document(
        self,
        connection_id,
        document: dict
    ):

        try:
            logger.info(f"Chunking document: {document}")
            ch = split_document_into_chunks(
                connection_id,
                document
            )

        except Exception as e:
            logger.error(f"Error occurred while chunking document: {e}")
            return None

        return ch

    def embed_document(
        self,
        document: dict,
        path: str,
        number_of_chunks: int = 0
    ):

        executor_params = {
            "client": {
                "host_url": self.connection_object.host_url,
                "api_key": self.connection_object.provider_api_key
            },
            "connection_id": self.connection_object.id
        }

        try:
            doc_id, doc_uuid, error = embed_document_data(
                executor_params=executor_params,
                document=document,
                path=path,
                number_of_chunks=number_of_chunks
            )
            logger.info(f"Embedded document successfully.")

        except Exception as e:
            logger.error(f"Error occurred while embedding document: {e}")
            return None, None, None

        return doc_id, doc_uuid, error

    def embed_document_chunks(
        self,
        chunks: list,
        path: str,
        document_id: int,
        document_uuid: str
    ):

        executor_params = {
            "client": {
                "host_url": self.connection_object.host_url,
                "api_key": self.connection_object.provider_api_key
            },
            "connection_id": self.connection_object.id
        }

        try:
            errors = embed_document_chunks(
                executor_params=executor_params,
                chunks=chunks, path=path,
                document_id=document_id,
                document_uuid=document_uuid
            )
            logger.info(f"Embedded document chunks successfully.")

        except Exception as e:
            logger.error(f"Error occurred while embedding document chunks: {e}")
            return

        return errors

    def search_hybrid(
        self,
        query: str,
        alpha: float
    ):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        class_name = f"{self.connection_object.class_name}Chunks"
        c = self.connect_c()
        collection = c.collections.get(class_name)

        vector_store_output = collection.query.hybrid(
            query_properties=[
                "chunk_document_file_name",
                "chunk_content"
            ],
            query=query,
            alpha=float(alpha),
            limit=int(self.connection_object.search_instance_retrieval_limit)
        )

        docs = []

        for o in vector_store_output.objects:

            instance_obj = {}
            if not o.properties:
                continue

            for k, v in o.properties.items():
                if k in [
                    "chunk_document_file_name",
                    "chunk_content",
                    "chunk_number",
                    "created_at"
                ]:
                    instance_obj[k] = v

            docs.append(instance_obj)

        try:
            tx = LLMTransaction(
                organization=self.connection_object.assistant.organization,
                model=self.connection_object.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection_object.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.KnowledgeBaseExecutor.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.KNOWLEDGE_BASE_SEARCH,
                is_tool_cost=True
            )
            tx.save()
            logger.info(f"Transaction saved successfully.")

        except Exception as e:
            logger.error(f"Error occurred while saving transaction: {e}")
            return None

        return docs
