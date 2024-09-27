from langchain_community.document_loaders import JSONLoader


def load_json_helper(path: str):
    loader = JSONLoader(file_path=path, jq_schema=".", text_content=False)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        for doc in docs:
            try:
                page_content = doc.page_content
                metadata = doc.metadata
                clean_doc["page_content"] += json.dumps(page_content, default=str, sort_keys=True)
                clean_doc["metadata"] = metadata
            except Exception as e:
                print(f"[tasks.load_json_helper] Error loading JSON: {e}")
                continue
    return clean_doc
