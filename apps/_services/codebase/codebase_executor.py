#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: codebase_executor.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: codebase_executor.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:03:12
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import os
from uuid import uuid4

import weaviate
import weaviate.classes as wvc
from weaviate.config import AdditionalConfig, Timeout

from apps._services.codebase.helpers.class_creator import create_classes_helper
from apps._services.codebase.helpers.class_deleter import delete_weaviate_class_helper
from apps._services.codebase.helpers.repository_deleter import delete_repository_helper
from apps._services.codebase.utils import WEAVIATE_INITIALIZATION_TIMEOUT, WEAVIATE_QUERY_TIMEOUT, \
    WEAVIATE_INSERT_TIMEOUT
from apps._services.config.costs_map import ToolCostsMap
from apps.datasource_codebase.tasks import embed_repository_chunks, embed_repository_data, \
    split_repository_into_chunks, index_repository_helper
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames


class WeaviateExecutor:

    def __init__(self, connection):
        self.connection_object = connection
        self.client = None

    def connect_c(self):
        try:
            c = weaviate.connect_to_weaviate_cloud(
                cluster_url=self.connection_object.host_url,
                auth_credentials=weaviate.auth.AuthApiKey(api_key=self.connection_object.provider_api_key),
                headers={"X-OpenAI-Api-Key": self.connection_object.vectorizer_api_key},
                additional_config=AdditionalConfig(
                    timeout=Timeout(init=WEAVIATE_INITIALIZATION_TIMEOUT,
                                    query=WEAVIATE_QUERY_TIMEOUT,
                                    insert=WEAVIATE_INSERT_TIMEOUT)))
            self.client = c
        except Exception as e:
            print(f"[WeaviateExecutor.connect_c] Error connecting to Weaviate: {e}")
            return self.client
        return self.client

    def close_c(self):
        try:
            self.client.close()
        except Exception as e:
            print(f"[WeaviateExecutor.close_c] Error closing the Weaviate connection: {e}")
            pass
        return

    def retrieve_schema(self):
        try:
            c = self.connect_c()
            # retrieve the schema for weaviate
            schema = c.collections.list_all()
            self.close_c()
        except Exception as e:
            print(f"Error retrieving Weaviate schema: {e}")
            return None
        return schema

    @staticmethod
    def decode_vectorizer(vectorizer_name):
        from apps.assistants.utils import VectorizerNames
        if vectorizer_name == VectorizerNames.TEXT2VEC_OPENAI:
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        else:
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################

    def create_weaviate_classes(self):
        try:
            _ = self.connect_c()
            output = create_classes_helper(executor=self)
            self.close_c()
        except Exception as e:
            print(f"[WeaviateExecutor.create_weaviate_classes] Error creating classes: {e}")
            return None
        return output

    def delete_weaviate_classes(self, class_name: str):
        try:
            _ = self.connect_c()
            output = delete_weaviate_class_helper(executor=self, class_name=class_name)
            self.close_c()
        except Exception as e:
            print(f"[WeaviateExecutor.delete_weaviate_classes] Error deleting classes: {e}")
            return None
        return output

    def delete_weaviate_repository(self, class_name: str, document_uuid: str):
        try:
            _ = self.connect_c()
            output = delete_repository_helper(executor=self, class_name=class_name, document_uuid=document_uuid)
            self.close_c()
        except Exception as e:
            print(f"[WeaviateExecutor.delete_weaviate_repository] Error deleting repository: {e}")
            return None
        return output

    def index_repositories(self, document_paths: list | str):
        try:
            _ = self.connect_c()
            index_repository_helper.delay(connection_id=self.connection_object.id, document_paths=document_paths)
            self.close_c()
        except Exception as e:
            print(f"[WeaviateExecutor.index_repositories] Error indexing repositories: {e}")
            return None
        return

    def repository_loader(self, file_path) -> dict | None:
        result = {
            "page_content": "",
            "metadata": {},
        }
        formatted_content = ""
        cloned_repository_path = self._clone_repository(repository_url=file_path)
        if not cloned_repository_path:
            print(f"[WeaviateExecutor.repository_loader] Error cloning the repository: {file_path}")
            return None
        try:
            for root, dirs, files in os.walk(cloned_repository_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.is_supported_file(file_path):
                        print(f"[WeaviateExecutor.repository_loader] Skipping unsupported file: {file_path}")
                        continue
                    content_lines = self.extract_file_content_and_metadata(file_path)
                    if not content_lines:
                        print(f"[WeaviateExecutor.repository_loader] No content extracted from file: {file_path}")
                        continue
                    formatted_content = self.assign_line_numbers_and_filename_to_line(str(file_path), content_lines)
        except Exception as e:
            print(f"[WeaviateExecutor.repository_loader] Error loading the repository: {e}")
            return None
        print(f"[WeaviateExecutor.repository_loader] Loaded the repository & contents successfully.")
        result["page_content"] = formatted_content
        print(f"[WeaviateExecutor.repository_loader] Full Content: \n\n {result['page_content']}")
        return result

    @staticmethod
    def _clone_repository(repository_url: str) -> str:
        uuid_str = str(uuid4())
        assigned_path = f"/tmp/{uuid_str}"
        try:
            os.system(f"git clone {repository_url} {assigned_path}")
        except Exception as e:
            print(f"[WeaviateExecutor._clone_repository] Error cloning the repository: {e}")
            return None
        return assigned_path

    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        from apps.datasource_codebase.utils import SupportedCodeFileTypes
        supported_files = SupportedCodeFileTypes.as_list()
        file_extension = "." + file_path.split(".")[-1]
        if file_extension in supported_files:
            return True
        return False

    @staticmethod
    def extract_file_content_and_metadata(file_path: str) -> list[str] | None:
        content = []
        # read line by line
        try:
            with open(file_path, "r") as f:
                content = f.readlines()
        except Exception as e:
            print(f"[WeaviateExecutor.extract_file_content_and_metadata] Error extracting content from file: {e}")
        print(
            f"[WeaviateExecutor.extract_file_content_and_metadata] Successfully extracted content from file: {file_path}")
        return content

    @staticmethod
    def assign_line_numbers_and_filename_to_line(file_path: str, content: list) -> str:
        accumulated_content = ""
        try:
            for i, line in enumerate(content):
                accumulated_content += f"[File Path: {file_path}] | [Line Number: {i}] --- {line}"
        except Exception as e:
            print(f"[WeaviateExecutor.assign_line_numbers_and_filename_to_line] Error assigning line numbers and "
                  f"filename to line: {e}")
            return accumulated_content
        return accumulated_content

    def chunk_repository(self, connection_id, document: dict):
        try:
            chunks = split_repository_into_chunks(connection_id, document)
        except Exception as e:
            print(f"[WeaviateExecutor.chunk_document] Error chunking the document: {e}")
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
        except Exception as e:
            print(f"[WeaviateExecutor.embed_document] Error embedding the document: {e}")
            return None, None, None
        return doc_id, doc_uuid, error

    def embed_repository_chunks(self, chunks: list, path: str, document_id: int, document_uuid: str):
        executor_params = {
            "client": {"host_url": self.connection_object.host_url,
                       "api_key": self.connection_object.provider_api_key},
            "connection_id": self.connection_object.id}
        try:
            errors = embed_repository_chunks(executor_params=executor_params, chunks=chunks, path=path,
                                             document_id=document_id, document_uuid=document_uuid)
        except Exception as e:
            print(f"[WeaviateExecutor.embed_document_chunks] Error embedding the document chunks: {e}")
            return
        return errors

    def search_hybrid(self, query: str, alpha: float):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
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

        try:
            transaction = LLMTransaction(
                organization=self.connection_object.assistant.organization,
                model=self.connection_object.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection_object.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.CodeBaseExecutor.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.CODE_BASE_SEARCH,
                is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            print(f"[WeaviateExecutor.search_hybrid] Error occurred while saving the transaction: {str(e)}")
            return None
        return cleaned_documents
