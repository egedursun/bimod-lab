import json

from celery import shared_task
from langchain_community.document_loaders import (PyPDFLoader, UnstructuredHTMLLoader, Docx2txtLoader,
                                                  NotebookLoader, JSONLoader, UnstructuredXMLLoader,
                                                  UnstructuredMarkdownLoader, UnstructuredRTFLoader,
                                                  UnstructuredODTLoader, UnstructuredPowerPointLoader,
                                                  UnstructuredExcelLoader)
from langchain_community.document_loaders.csv_loader import UnstructuredCSVLoader


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
    loader = UnstructuredCSVLoader(file_path=path, mode="elements")
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
# CHUNKERS
############################################################################################################


@shared_task
def split_document_into_chunks():
    pass
