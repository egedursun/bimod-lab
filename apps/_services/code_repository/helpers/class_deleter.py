

def delete_weaviate_class_helper(executor, class_name):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete - Code Repository Class
        r = c.collections.delete(class_name)
        # Delete - Code repository chunks class
        r = c.collections.delete(f"{class_name}Chunks")
    except Exception as e:
        output["status"] = False
        output["error"] = f"Error deleting code repository classes: {e}"
    return output
