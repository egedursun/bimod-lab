from langchain_community.document_loaders import Docx2txtLoader


def load_docx_helper(path: str):
    loader = Docx2txtLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        for doc in docs:
            try:
                page_content = doc.page_content
                metadata = doc.metadata
                clean_doc["page_content"] += page_content
                clean_doc["metadata"] = metadata
            except Exception as e:
                print(f"[tasks.load_docx_helper] Error loading DOCX: {e}")
                continue
    return clean_doc
