import json

from celery import shared_task
from langchain_community.document_loaders import (PyPDFLoader, UnstructuredHTMLLoader, Docx2txtLoader,
                                                  NotebookLoader, JSONLoader, UnstructuredXMLLoader,
                                                  UnstructuredMarkdownLoader, UnstructuredRTFLoader,
                                                  UnstructuredODTLoader, UnstructuredPowerPointLoader,
                                                  UnstructuredExcelLoader)
from langchain_community.document_loaders.csv_loader import UnstructuredCSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from apps._services.knowledge_base.document.helpers.document_chunk_embedder import embed_document_chunks_helper
from apps._services.knowledge_base.document.helpers.document_embedder import embed_document_helper


############################################################################################################
# INDEX
############################################################################################################

def add_document_upload_log(document_full_uri, log_name):
    from apps.datasource_knowledge_base.models import DocumentProcessingLog, DocumentUploadStatusNames
    DocumentProcessingLog.objects.create(
        document_full_uri=document_full_uri,
        log_message=log_name
    )

@shared_task
def index_document_helper(connection_id, document_paths):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import DocumentProcessingLog, DocumentUploadStatusNames

    connection = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = KnowledgeBaseSystemDecoder.get(connection=connection)
    ##################################################
    if isinstance(document_paths, str):
        document_paths = [document_paths]
    # Iterate through the documents
    print(f"Indexing {len(document_paths)} document(s)...")
    print(document_paths)
    for i, path in enumerate(document_paths):
        print(f"Indexing document [{i+1}] of [{len(document_paths)}] with path: {path}")
        try:
            # Get the file extension
            extension = path.split(".")[-1]
            print(f"Filename: {path.split('/')[-1]}")
            print(f"Identified file extension: {extension}")
            # Load the document
            print("Loading document...")
            document = executor.document_loader(file_path=path, file_type=extension)
            if not document:
                print(f"Error loading the document with path: {path}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.LOADED)

            # Chunk the document
            print("Preparing document for chunking...")
            chunks = executor.chunk_document(connection_id=executor.connection_object.id, document=document)
            if not chunks:
                print(f"Error chunking the document with path: {path}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.CHUNKED)

            print("Calculating number of chunks...")
            number_of_chunks = len(chunks) if chunks else 0
            print(f"Identified number of chunks: {number_of_chunks}")

            # Embed the document
            print("Embedding document...")
            doc_id, doc_uuid, error = executor.embed_document(
                document=document, path=path, number_of_chunks=number_of_chunks
            )
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PROCESSED_DOCUMENT)

            print(f"Document ID: {doc_id}")
            if error or not doc_id or not doc_uuid:
                print(f"Error embedding the document with path: {path} - Error: {error}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue

            # Embed the document chunks
            print("Embedding document chunks...")
            errors = executor.embed_document_chunks(chunks=chunks, path=path, document_id=doc_id,
                                                    document_uuid=doc_uuid)
            if errors:
                print(f"Error embedding at least one of the document chunks with the document path: {path} -"
                      f" Error: {errors}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PARTIALLY_FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PROCESSED_CHUNKS)

            print(f"Document with path: {path} successfully indexed.")
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.COMPLETED)

        except Exception as e:
            print(f"Error indexing the document with path: {path} - Error: {e}")
            continue
    # make sure that the return statement is outside the loop
    return


############################################################################################################
# LOADERS
############################################################################################################

def load_pdf_helper(path: str):
    loader = PyPDFLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading PDF: {e}")
            pass
    return clean_doc

def load_html_helper(path: str):
    loader = UnstructuredHTMLLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading HTML: {e}")
            pass
    return clean_doc

def load_csv_helper(path: str):
    loader = UnstructuredCSVLoader(file_path=path, mode="single")
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
            return clean_doc
        except Exception as e:
            print(f"Error loading CSV: {e}")
            pass
    return clean_doc

def load_docx_helper(path: str):
    loader = Docx2txtLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading DOCX: {e}")
            pass
    return clean_doc

def load_ipynb_helper(path: str):
    loader = NotebookLoader(path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading IPYNB: {e}")
            pass
    return clean_doc

def load_json_helper(path: str):
    loader = JSONLoader(file_path=path, jq_schema=".", text_content=False)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = json.dumps(page_content, default=str, sort_keys=True)
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading JSON: {e}")
            pass
    return clean_doc

def load_xml_helper(path: str):
    loader = UnstructuredXMLLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading XML: {e}")
            pass
    return clean_doc

def load_txt_helper(path: str):
    clean_doc = {"page_content": "", "metadata": {}}
    with open(path, "r") as f:
        content = f.read()
        clean_doc["page_content"] = content
        clean_doc["metadata"] = {
            "file_name": path.split("/")[-1],
            "file_path": path,
            "file_char_size": len(content)
        }
    return clean_doc

def load_md_helper(path: str):
    loader = UnstructuredMarkdownLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading MD: {e}")
            pass
    return clean_doc

def load_rtf_helper(path: str):
    loader = UnstructuredRTFLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading RTF: {e}")
            pass
    return clean_doc

def load_odt_helper(path: str):
    loader = UnstructuredODTLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading ODT: {e}")
            pass
    return clean_doc

def load_pptx_helper(path: str):
    loader = UnstructuredPowerPointLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading PPTX: {e}")
            pass
    return clean_doc

def load_xlsx_helper(path: str):
    loader = UnstructuredExcelLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        doc = docs[0]
        try:
            page_content = doc.page_content
            metadata = doc.metadata
            clean_doc["page_content"] = page_content
            clean_doc["metadata"] = metadata
        except Exception as e:
            print(f"Error loading XLSX: {e}")
            pass
    return clean_doc


############################################################################################################
# EMBEDDERS
############################################################################################################

def embed_document_data(executor_params, document, path, number_of_chunks):
    doc_id, doc_uuid = None, None
    try:
        print("Calling embed_document_helper...")
        doc_id, doc_uuid, error = embed_document_helper(
            executor_params=executor_params,
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
        print(f"Document ID: {doc_id}")
    except Exception as e:
        error = f"Error embedding the document: {e}"
    return doc_id, doc_uuid, error


def embed_document_chunks(executor_params, chunks, path, document_id, document_uuid):
    try:
        error = embed_document_chunks_helper(
            executor_params=executor_params,
            chunks=chunks,
            path=path,
            document_id=document_id,
            document_uuid=document_uuid
        )
    except Exception as e:
        error = f"Error embedding the document chunks: {e}"
    return error


############################################################################################################
# CHUNKERS
############################################################################################################

def split_document_into_chunks(connection_id, doc):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    connection = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=connection.embedding_chunk_size, chunk_overlap=connection.embedding_chunk_overlap
    )
    chunks = splitter.split_text(doc["page_content"])
    clean_chunks = []
    for i, chunk in enumerate(chunks):
        doc["metadata"]["chunk_index"] = i
        clean_chunk = {
            "page_content": chunk,
            "metadata": doc["metadata"]
        }
        clean_chunks.append(clean_chunk)
    print(f"Document chunked into {len(clean_chunks)} chunk(s).")
    return clean_chunks

############################################################################################################
