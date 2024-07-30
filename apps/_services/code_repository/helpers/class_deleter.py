

def delete_code_repository_class_helper(executor, class_name):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete - Document class
        r = c.collections.delete(class_name)
        # Delete - Document Chunks class
        r = c.collections.delete(f"{class_name}Chunks")
    except Exception as e:
        output["status"] = False
        output["error"] = f"Error deleting code repository Weaviate classes: {e}"
    return output
