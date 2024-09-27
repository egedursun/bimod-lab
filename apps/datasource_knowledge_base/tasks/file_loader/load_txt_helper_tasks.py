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
