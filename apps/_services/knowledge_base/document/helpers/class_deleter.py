

def delete_weaviate_class_helper(executor, class_name):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete - Document class
        r = c.collections.delete(class_name)
        # Delete - Document Chunks class
        r = c.collections.delete(f"{class_name}Chunks")
    except Exception as e:
        output["status"] = False
        output["error"] = f"Error deleting classes: {e}"
    return output


def delete_chat_history_class_helper(executor, class_name):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete - Context history class
        r = c.collections.delete(class_name)
        # Delete - Context history Chunks class
        r = c.collections.delete(f"{class_name}Chunks")
    except Exception as e:
        output["status"] = False
        output["error"] = f"Error deleting chat history classes: {e}"
    return output
