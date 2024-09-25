
from weaviate.classes.query import Filter


def delete_repository_helper(executor, class_name: str, document_uuid):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete the repository
        _ = c.collections.get(class_name).data.delete_by_id(document_uuid)
        # Delete the chunks of repository
        _ = c.collections.get(f"{class_name}Chunks").data.delete_many(
            where=Filter.by_property("repository_uuid").equal(document_uuid)
        )
        print(f"[repository_deleter.delete_repository_helper] Deleted repository: {document_uuid}")
    except Exception as e:
        output["status"] = False
        output["error"] = f"[repository_deleter.delete_repository_helper] Error deleting repository: {e}"
    return output
