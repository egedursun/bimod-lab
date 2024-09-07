

def delete_weaviate_class_helper(executor, class_name):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # delete Codebase Repository class
        r = c.collections.delete(class_name)
        # delete Chunks class
        r = c.collections.delete(f"{class_name}Chunks")
        print(f"[class_deleter.delete_weaviate_class_helper] Deleted Weaviate classes: {class_name} and {class_name}Chunks")
    except Exception as e:
        output["status"] = False
        output["error"] = f"[class_deleter.delete_weaviate_class_helper] Error deleting classes: {e}"
    return output
