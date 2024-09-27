from langchain_community.document_loaders import UnstructuredExcelLoader


def load_xlsx_helper(path: str):
    loader = UnstructuredExcelLoader(file_path=path)
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
                print(f"[tasks.load_xlsx_helper] Error loading XLSX: {e}")
                continue
    return clean_doc
