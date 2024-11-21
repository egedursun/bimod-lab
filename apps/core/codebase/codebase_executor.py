#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: codebase_executor.py
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
import os
from uuid import uuid4

import weaviate
import weaviate.classes as wvc
from weaviate.config import AdditionalConfig, Timeout

from apps.core.codebase.handler_methods.creation_handler import create_classes_helper
from apps.core.codebase.handler_methods.removal_handler import delete_weaviate_class_helper
from apps.core.codebase.handler_methods.removal_handler_repo import delete_repository_helper
from apps.core.codebase.utils import WEAVIATE_INITIALIZATION_TIMEOUT, WEAVIATE_QUERY_TIMEOUT, \
    WEAVIATE_INSERT_TIMEOUT
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.datasource_codebase.tasks import embed_repository_chunks, embed_repository_data, \
    split_repository_into_chunks, index_repository_helper
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
                        insert=WEAVIATE_INSERT_TIMEOUT
                    )
                )
            )
            logger.info(
                f"[WeaviateExecutor.connect_c] Connected to Weaviate cluster: {self.connection_object.host_url}")
            self.client = c

        except Exception as e:
            logger.error(f"[WeaviateExecutor.connect_c] Error connecting to Weaviate cluster: {e}")
            return self.client

        return self.client

    def close_c(self):
        try:
            logger.info(f"[WeaviateExecutor.close_c] Closing Weaviate connection")
            self.client.close()

        except Exception as e:
            logger.error(f"[WeaviateExecutor.close_c] Error closing Weaviate connection: {e}")
            pass

        return

    def retrieve_schema(self):
        try:
            c = self.connect_c()
            schema = c.collections.list_all()
            logger.info(f"[WeaviateExecutor.retrieve_schema] Retrieved Weaviate schema")
            self.close_c()

        except Exception as e:
            logger.error(f"[WeaviateExecutor.retrieve_schema] Error retrieving Weaviate schema: {e}")
            return None

        return schema

    @staticmethod
    def decode_vectorizer(vectorizer_name):
        from apps.assistants.utils import EmbeddingManagersNames

        if vectorizer_name == EmbeddingManagersNames.TEXT2VEC_OPENAI:
            logger.info(f"[WeaviateExecutor.decode_vectorizer] Decoding vectorizer: {vectorizer_name}")
            return wvc.config.Configure.Vectorizer.text2vec_openai()

        else:
            logger.info(f"[WeaviateExecutor.decode_vectorizer] Decoding vectorizer: {vectorizer_name}")
            return wvc.config.Configure.Vectorizer.text2vec_openai()

    def create_weaviate_classes(self):
        try:
            _ = self.connect_c()
            output = create_classes_helper(executor=self)
            logger.info(f"[WeaviateExecutor.create_weaviate_classes] Created Weaviate classes")
            self.close_c()

        except Exception as e:
            logger.error(f"[WeaviateExecutor.create_weaviate_classes] Error creating Weaviate classes: {e}")
            return None

        return output

    def delete_weaviate_classes(self, class_name: str):
        try:
            _ = self.connect_c()
            logger.info(f"[WeaviateExecutor.delete_weaviate_classes] Deleting Weaviate class: {class_name}")
            output = delete_weaviate_class_helper(executor=self, class_name=class_name)
            self.close_c()

        except Exception as e:
            logger.error(f"[WeaviateExecutor.delete_weaviate_classes] Error deleting Weaviate class: {e}")
            return None

        return output

    def delete_weaviate_repository(
        self,
        class_name: str,
        document_uuid: str
    ):
        try:
            _ = self.connect_c()
            logger.info(f"[WeaviateExecutor.delete_weaviate_repository] Deleting Weaviate repository: {document_uuid}")
            output = delete_repository_helper(
                executor=self,
                class_name=class_name,
                document_uuid=document_uuid
            )
            self.close_c()

        except Exception as e:
            logger.error(f"[WeaviateExecutor.delete_weaviate_repository] Error deleting Weaviate repository: {e}")
            return None

        return output

    def index_repositories(self, document_paths: list | str):
        try:
            _ = self.connect_c()
            logger.info(f"[WeaviateExecutor.index_repositories] Indexing repositories: {document_paths}")
            index_repository_helper.delay(
                connection_id=self.connection_object.id,
                document_paths=document_paths
            )
            self.close_c()

        except Exception as e:
            logger.error(f"[WeaviateExecutor.index_repositories] Error indexing repositories: {e}")
            return None

        return

    def repository_loader(self, file_path) -> dict | None:

        result = {"page_content": "", "metadata": {}}
        formatted_content = ""
        cloned_repository_path = self._clone_repository(
            repository_url=file_path
        )

        if not cloned_repository_path:
            logger.error(f"[WeaviateExecutor.repository_loader] Error cloning repository: {file_path}")
            return None

        try:
            for root, dirs, files in os.walk(cloned_repository_path):
                for file in files:
                    file_path = os.path.join(root, file)

                    if not self.is_supported_file(file_path):
                        logger.info(f"[WeaviateExecutor.repository_loader] Skipping unsupported file: {file_path}")
                        continue

                    content_lines = self.extract_file_content_and_metadata(file_path)
                    if not content_lines:
                        logger.error(
                            f"[WeaviateExecutor.repository_loader] Error extracting file content: {file_path}")
                        continue

                    formatted_content += self.assign_line_numbers_and_filename_to_line(str(file_path), content_lines)
                    formatted_content += "\n"
                    logger.info(f"[WeaviateExecutor.repository_loader] Loaded file: {file_path}")

        except Exception as e:
            logger.error(f"[WeaviateExecutor.repository_loader] Error loading repository: {file_path}")
            return None

        result["page_content"] = formatted_content
        logger.info(f"[WeaviateExecutor.repository_loader] Loaded repository: {file_path}")
        return result

    @staticmethod
    def _clone_repository(repository_url: str) -> str:
        uuid_str = str(uuid4())
        assigned_path = f"/tmp/{uuid_str}"
        try:
            os.system(f"git clone {repository_url} {assigned_path}")
            logger.info(f"[WeaviateExecutor._clone_repository] Cloned repository: {repository_url}")
        except Exception as e:
            logger.error(f"[WeaviateExecutor._clone_repository] Error cloning repository: {repository_url}")
            return None
        return assigned_path

    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        from apps.datasource_codebase.utils import SupportedCodeFileTypes
        supported_files = SupportedCodeFileTypes.as_list()
        file_extension = "." + file_path.split(".")[-1]
        if file_extension in supported_files:
            logger.info(f"[WeaviateExecutor.is_supported_file] Supported file: {file_path}")
            return True
        logger.info(f"[WeaviateExecutor.is_supported_file] Unsupported file: {file_path}")
        return False

    @staticmethod
    def extract_file_content_and_metadata(file_path: str) -> list[str] | None:
        content = []
        try:
            with open(file_path, "r") as f:
                content = f.readlines()
        except Exception as e:
            logger.error(
                f"[WeaviateExecutor.extract_file_content_and_metadata] Error extracting file content: {file_path}")
            pass
        return content

    @staticmethod
    def assign_line_numbers_and_filename_to_line(file_path: str, content: list) -> str:
        accumulated_content = ""
        try:
            for i, line in enumerate(content):
                accumulated_content += f"[File Path: {file_path}] | [Line Number: {i}] --- {line}"
        except Exception as e:
            logger.error(f"[WeaviateExecutor.assign_line_numbers_and_filename_to_line] Error assigning line numbers "
                         f"and filename to line: {file_path}")
            return accumulated_content
        logger.info(f"[WeaviateExecutor.assign_line_numbers_and_filename_to_line] Assigned line numbers and "
                    f"filename to line: {file_path}")
        return accumulated_content

    def chunk_repository(self, connection_id, document: dict):
        try:
            chunks = split_repository_into_chunks(connection_id, document)
            logger.info(f"[WeaviateExecutor.chunk_repository] Chunked the repository")
        except Exception as e:
            logger.error(f"[WeaviateExecutor.chunk_repository] Error chunking the repository: {e}")
            return None
        return chunks

    def embed_repository(self, document: dict, path: str, number_of_chunks: int = 0):
        executor_params = {"client": {"host_url": self.connection_object.host_url,
                                      "api_key": self.connection_object.provider_api_key},
                           "connection_id": self.connection_object.id}
        try:
            doc_id, doc_uuid, error = embed_repository_data(executor_params=executor_params, document=document,
                                                            path=path,
                                                            number_of_chunks=number_of_chunks)
            logger.info(f"[WeaviateExecutor.embed_repository] Embedded the repository")
        except Exception as e:
            logger.error(f"[WeaviateExecutor.embed_repository] Error embedding the repository: {e}")
            return None, None, None
        return doc_id, doc_uuid, error

    def embed_repository_chunks(self, chunks: list, path: str, document_id: int, document_uuid: str):
        executor_params = {
            "client": {
                "host_url": self.connection_object.host_url,
                "api_key": self.connection_object.provider_api_key
            },
            "connection_id": self.connection_object.id
        }
        try:
            errors = embed_repository_chunks(executor_params=executor_params, chunks=chunks, path=path,
                                             document_id=document_id, document_uuid=document_uuid)
            logger.info(f"[WeaviateExecutor.embed_repository_chunks] Embedded the repository chunks")
        except Exception as e:
            logger.error(f"[WeaviateExecutor.embed_repository_chunks] Error embedding the repository chunks: {e}")
            return
        return errors

    def search_hybrid(self, query: str, alpha: float):
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        search_vector_store_class_name = f"{self.connection_object.class_name}Chunks"
        client = self.connect_c()
        documents_collection = client.collections.get(search_vector_store_class_name)
        response = documents_collection.query.hybrid(
            query_properties=["chunk_repository_file_name", "chunk_content"],
            query=query, alpha=float(alpha), limit=int(self.connection_object.search_instance_retrieval_limit))
        cleaned_documents = []
        for o in response.objects:
            cleaned_object = {}
            if not o.properties:
                logger.info(f"[WeaviateExecutor.search_hybrid] Skipping empty object")
                continue
            for k, v in o.properties.items():
                if k in ["chunk_repository_file_name", "chunk_content", "chunk_number", "created_at"]:
                    cleaned_object[k] = v
            cleaned_documents.append(cleaned_object)

        try:
            tx = LLMTransaction(
                organization=self.connection_object.assistant.organization,
                model=self.connection_object.assistant.llm_model, responsible_user=None,
                responsible_assistant=self.connection_object.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.CodeBaseExecutor.COST, transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.CODE_BASE_SEARCH, is_tool_cost=True)
            tx.save()
            logger.info(f"[WeaviateExecutor.search_hybrid] Saved LLM Transaction: {tx.id}")
        except Exception as e:
            logger.error(f"[WeaviateExecutor.search_hybrid] Error saving LLM Transaction: {e}")
            return None
        return cleaned_documents
