import weaviate
import weaviate.classes as wvc

from apps._services.knowledge_base.document.helpers.class_creator import create_classes_helper
from apps.assistants.models import VectorizerNames
from apps.datasource_knowledge_base.tasks import load_csv_helper, load_pdf_helper, load_html_helper, load_docx_helper, \
    load_ipynb_helper, load_json_helper, load_xml_helper, load_txt_helper, load_md_helper, load_rtf_helper, \
    load_odt_helper, load_pptx_helper, load_xlsx_helper


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
                auth_credentials=weaviate.auth.AuthApiKey(api_key=weaviate_api_key)
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

    def index_documents(self):
        ##################################################
        # TODO: WRAPPER method
        pass
        ##################################################

    def file_type_decoder(self, file_type):
        # TODO:-X: implement the file type decoder to understand the file type and use the appropriate methods
        if file_type == SupportedDocumentTypesNames.PDF: load_pdf_helper.delay()
        elif file_type == SupportedDocumentTypesNames.HTML: load_html_helper.delay()
        elif file_type == SupportedDocumentTypesNames.CSV: load_csv_helper.delay()
        elif file_type == SupportedDocumentTypesNames.DOCX: load_docx_helper.delay()
        elif file_type == SupportedDocumentTypesNames.IPYNB: load_ipynb_helper.delay()
        elif file_type == SupportedDocumentTypesNames.JSON: load_json_helper.delay()
        elif file_type == SupportedDocumentTypesNames.XML: load_xml_helper.delay()
        elif file_type == SupportedDocumentTypesNames.TXT: load_txt_helper.delay()
        elif file_type == SupportedDocumentTypesNames.MD: load_md_helper.delay()
        elif file_type == SupportedDocumentTypesNames.RTF: load_rtf_helper.delay()
        elif file_type == SupportedDocumentTypesNames.ODT: load_odt_helper.delay()
        elif file_type == SupportedDocumentTypesNames.POWERPOINT: load_pptx_helper.delay()
        elif file_type == SupportedDocumentTypesNames.XLSX: load_xlsx_helper.delay()
        else: print("[File Type Decoder]: Unsupported file type for the document.")

    def load_document(self):
        # TODO: step-1 load the document
        pass

    def embed_document(self):
        # TODO: step-2 embed the document
        pass

    def chunk_document(self):
        # TODO: step-2 chunk the document [retrieve CHUNKS]
        pass

    def embed_document_chunks(self):
        # TODO: step-3 embed the chunks
        pass
