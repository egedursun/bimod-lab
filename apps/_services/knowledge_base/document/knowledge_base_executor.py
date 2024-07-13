import weaviate
import weaviate.classes as wvc

from apps._services.knowledge_base.document.helpers.class_creator import create_classes_helper
from apps.assistants.models import VectorizerNames
from apps.datasource_knowledge_base.tasks import load_csv_helper, load_pdf_helper, load_html_helper, load_docx_helper, \
    load_ipynb_helper, load_json_helper, load_xml_helper, load_txt_helper, load_md_helper, load_rtf_helper, \
    load_odt_helper, load_pptx_helper, load_xlsx_helper, split_document_into_chunks, embed_document_data, \
    embed_document_chunks

TASK_PROCESSING_TIMEOUT_SECONDS = (60 * 15)  # 15 minutes


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
        host_url = self.connection_object.host_url
        weaviate_api_key = self.connection_object.provider_api_key
        try:
            c = weaviate.connect_to_weaviate_cloud(
                cluster_url=host_url,
                auth_credentials=weaviate.auth.AuthApiKey(api_key=weaviate_api_key),
                headers={
                    "X-OpenAI-Api-Key": connection.vectorizer_api_key
                }
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
        output = create_classes_helper(executor=self)
        self.close_connection()
        return output

    def index_documents(self, document_paths: list|str):
        ##################################################
        if isinstance(document_paths, str):
            document_paths = [document_paths]
        # Iterate through the documents
        for path in document_paths:
            try:
                # Get the file extension
                extension = path.split(".")[-1]
                # Load the document
                document = self.document_loader(file_path=path, file_type=extension)

                # Chunk the document
                chunks = self.chunk_document(document)
                number_of_chunks = len(chunks) if chunks else 0

                # Embed the document
                doc_id, error = self.embed_document(document=document, path=path, number_of_chunks=number_of_chunks)
                if error:
                    print(f"Error embedding the document with path: {path} - Error: {error}")
                    continue

                # Embed the document chunks
                errors = self.embed_document_chunks(chunks=chunks, path=path, document_id=doc_id)
                if errors:
                    print(f"Error embedding at least one of the document chunks with the document path: {path} -"
                          f" Error: {errors}")
                    continue

            except Exception as e:
                print(f"Error indexing the document with path: {path} - Error: {e}")
                continue

        ##################################################

    def document_loader(self, file_path, file_type):
        d = None
        if file_type == SupportedDocumentTypesNames.PDF: d = load_pdf_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.HTML: d = load_html_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.CSV: d = load_csv_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.DOCX: d = load_docx_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.IPYNB: d = load_ipynb_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.JSON: d = load_json_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.XML: d = load_xml_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.TXT: d = load_txt_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.MD: d = load_md_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.RTF: d = load_rtf_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.ODT: d = load_odt_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.POWERPOINT: d = load_pptx_helper.delay(path=file_path)
        elif file_type == SupportedDocumentTypesNames.XLSX: d = load_xlsx_helper.delay(path=file_path)
        else: print("[File Type Decoder]: Unsupported file type for the document.")

        result = d.get(timeout=TASK_PROCESSING_TIMEOUT_SECONDS)
        return result

    def chunk_document(self, document: dict):
        chunks_task = split_document_into_chunks.delay(document)
        chunks = chunks_task.get(timeout=TASK_PROCESSING_TIMEOUT_SECONDS)
        return chunks

    def embed_document(self, document: dict, path: str, number_of_chunks: int = 0):
        executor_params = {
            "client": {
                "host_url": self.connection_object.host_url,
                "api_key": self.connection_object.provider_api_key
            },
            "connection_id": self.connection_object.id
        }
        embed_document_task = embed_document_data.delay(executor_params=executor_params, document=document, path=path,
                                                        number_of_chunks=number_of_chunks)
        doc_id, error = embed_document_task.get(timeout=TASK_PROCESSING_TIMEOUT_SECONDS)
        return doc_id, error

    def embed_document_chunks(self, chunks: list, path: str, document_id: int):
        executor_params = {
            "client": {
                "host_url": self.connection_object.host_url,
                "api_key": self.connection_object.provider_api_key
            },
            "connection_id": self.connection_object.id
        }
        embed_chunks_task = embed_document_chunks.delay(executor_params=executor_params, chunks=chunks, path=path,
                                                        document_id=document_id)
        errors = embed_chunks_task.get(timeout=TASK_PROCESSING_TIMEOUT_SECONDS)
        return errors
