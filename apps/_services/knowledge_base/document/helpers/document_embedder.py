from langchain_core.documents import Document

from apps._services.knowledge_base.document.knowledge_base_executor import WeaviateExecutor
# TODO: delete this importation later on as it might cause circular import issue
import langchain


def embed_document_helper(executor: WeaviateExecutor, document: Document):
    # TODO: implement the document embedding logic here
    pass
