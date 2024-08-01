import weaviate
import weaviate.classes as wvc
from weaviate.config import AdditionalConfig, Timeout

from apps._services.config.costs_map import ToolCostsMap
from apps._services.knowledge_base.document.helpers.class_creator import create_classes_helper
from apps._services.knowledge_base.document.helpers.class_deleter import delete_weaviate_class_helper
from apps._services.knowledge_base.document.helpers.document_deleter import delete_document_helper
from apps.datasource_knowledge_base.tasks import load_csv_helper, load_pdf_helper, load_html_helper, load_docx_helper, \
    load_ipynb_helper, load_json_helper, load_xml_helper, load_txt_helper, load_md_helper, load_rtf_helper, \
    load_odt_helper, load_pptx_helper, load_xlsx_helper, split_document_into_chunks, embed_document_data, \
    embed_document_chunks, index_document_helper
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames

TASK_PROCESSING_TIMEOUT_SECONDS = (60 * 60)  # 60 minutes for all the tasks for a pipeline to complete maximum
WEAVIATE_INITIALIZATION_TIMEOUT = 30  # 30 seconds for the weaviate initialization
WEAVIATE_QUERY_TIMEOUT = 60  # 60 seconds for the weaviate query
WEAVIATE_INSERT_TIMEOUT = 120  # 120 seconds for the weaviate insert


class SupportedDocumentTypesNames:
    PDF = 'pdf'
    HTML = 'html'
    CSV = 'csv'
    DOCX = 'docx'
    IPYNB = 'ipynb'
    JSON = 'json'
    XML = 'xml'
    TXT = 'txt'
    MD = 'md'
    RTF = 'rtf'
    ODT = 'odt'
    POWERPOINT = 'pptx'
    XLSX = 'xlsx'


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
            print(f"Error retrieving Weaviate schema: {e}")
            return None
        return schema

    @staticmethod
    def decode_vectorizer(vectorizer_name):
        from apps.assistants.models import VectorizerNames
        if vectorizer_name == VectorizerNames.TEXT2VEC_OPENAI:
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        else:
            return wvc.config.Configure.Vectorizer.text2vec_openai()
        ##################################################

    def create_weaviate_classes(self):
        _ = self.connect_c()
        output = create_classes_helper(executor=self)
        self.close_c()
        return output

    def delete_weaviate_classes(self, class_name: str):
        _ = self.connect_c()
        output = delete_weaviate_class_helper(executor=self, class_name=class_name)
        self.close_c()
        return output

    def delete_weaviate_document(self, class_name: str, document_uuid: str):
        _ = self.connect_c()
        output = delete_document_helper(executor=self, class_name=class_name, document_uuid=document_uuid)
        self.close_c()
        return output

    def index_documents(self, document_paths: list | str):
        _ = self.connect_c()
        index_document_helper.delay(connection_id=self.connection_object.id, document_paths=document_paths)
        self.close_c()
        return

    def document_loader(self, file_path, file_type):
        d = None
        if file_type == SupportedDocumentTypesNames.PDF:
            d = load_pdf_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.HTML:
            d = load_html_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.CSV:
            d = load_csv_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.DOCX:
            d = load_docx_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.IPYNB:
            d = load_ipynb_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.JSON:
            d = load_json_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.XML:
            d = load_xml_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.TXT:
            d = load_txt_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.MD:
            d = load_md_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.RTF:
            d = load_rtf_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.ODT:
            d = load_odt_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.POWERPOINT:
            d = load_pptx_helper(path=file_path)
        elif file_type == SupportedDocumentTypesNames.XLSX:
            d = load_xlsx_helper(path=file_path)
        else:
            print("[File Type Decoder]: Unsupported file type for the document.")
        result = d
        return result

    def chunk_document(self, connection_id, document: dict):
        chunks = split_document_into_chunks(connection_id, document)
        return chunks

    def embed_document(self, document: dict, path: str, number_of_chunks: int = 0):
        executor_params = {"client": {"host_url": self.connection_object.host_url,
                                      "api_key": self.connection_object.provider_api_key},
                           "connection_id": self.connection_object.id}
        doc_id, doc_uuid, error = embed_document_data(executor_params=executor_params, document=document, path=path,
                                                      number_of_chunks=number_of_chunks)
        return doc_id, doc_uuid, error

    def embed_document_chunks(self, chunks: list, path: str, document_id: int, document_uuid: str):
        executor_params = {
            "client": {"host_url": self.connection_object.host_url,
                       "api_key": self.connection_object.provider_api_key},
            "connection_id": self.connection_object.id}
        errors = embed_document_chunks(executor_params=executor_params, chunks=chunks, path=path,
                                       document_id=document_id, document_uuid=document_uuid)
        return errors

    def search_hybrid(self, query: str, alpha: float):
        from apps._services.llms.openai import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
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
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.KnowledgeBaseExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.KNOWLEDGE_BASE_SEARCH,
            is_tool_cost=True
        )
        transaction.save()
        return cleaned_documents
