from langchain_community.document_loaders import UnstructuredXMLLoader


def load_xml_helper(path: str):
    loader = UnstructuredXMLLoader(file_path=path)
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
                print(f"[tasks.load_xml_helper] Error loading XML: {e}")
                continue
    return clean_doc
