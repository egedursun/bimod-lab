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
# LOADERS
############################################################################################################


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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


@shared_task
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

@shared_task
def embed_document_data(executor_params, document, path, number_of_chunks):
    doc_id = None
    try:
        doc_id, error = embed_document_helper(
            executor_params=executor_params,
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
    except Exception as e:
        error = f"Error embedding the document: {e}"
    return doc_id, error


@shared_task
def embed_document_chunks(executor_params, chunks, path, document_id):
    try:
        error = embed_document_chunks_helper(
            executor_params=executor_params,
            chunks=chunks,
            path=path,
            document_id=document_id
        )
    except Exception as e:
        error = f"Error embedding the document chunks: {e}"
    return error

############################################################################################################
# CHUNKERS
############################################################################################################

@shared_task
def split_document_into_chunks(doc):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
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
    return clean_chunks


############################################################################################################
