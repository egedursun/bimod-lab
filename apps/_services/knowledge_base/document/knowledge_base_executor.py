import weaviate
import weaviate.classes as wvc

from apps._services.knowledge_base.document.helpers.class_creator import create_classes_helper
from apps.assistants.models import VectorizerNames


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
        # TODO: wrapper method
        pass
        ##################################################

    def file_type_decoder(self, file_type):
        # TODO:-X: implement the file type decoder to understand the file type and use the appropriate methods
        pass

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
