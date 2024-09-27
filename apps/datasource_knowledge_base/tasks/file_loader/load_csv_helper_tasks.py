from langchain_community.document_loaders import UnstructuredCSVLoader


def load_csv_helper(path: str):
    loader = UnstructuredCSVLoader(file_path=path, mode="single")
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        for doc in docs:
            try:
                page_content = doc.page_content
                metadata = doc.metadata
                clean_doc["page_content"] += page_content
                clean_doc["metadata"] = metadata
                return clean_doc
            except Exception as e:
                print(f"[tasks.load_csv_helper] Error loading CSV: {e}")
                continue
    return clean_doc
