
from weaviate.classes.query import Filter


def delete_repository_class_helper(executor, class_name: str, repository_uuid):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete the Code repository
        r = c.collections.get(class_name).data.delete_by_id(repository_uuid)
        # Delete the Code repository chunks
        r = c.collections.get(f"{class_name}Chunks").data.delete_many(
            where=Filter.by_property("document_uuid").equal(repository_uuid)
        )

    except Exception as e:
        output["status"] = False
        output["error"] = f"Error deleting code repository classes: {e}"
    return output
