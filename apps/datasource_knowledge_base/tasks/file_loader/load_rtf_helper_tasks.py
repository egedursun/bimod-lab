from langchain_community.document_loaders import UnstructuredRTFLoader


def load_rtf_helper(path: str):
    loader = UnstructuredRTFLoader(file_path=path)
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
                print(f"[tasks.load_rtf_helper] Error loading RTF: {e}")
                continue
    return clean_doc
