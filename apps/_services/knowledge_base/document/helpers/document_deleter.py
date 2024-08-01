
from weaviate.classes.query import Filter


def delete_document_helper(executor, class_name: str, document_uuid):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete the document
        r = c.collections.get(class_name).data.delete_by_id(document_uuid)
        # Delete the chunks of document
        r = c.collections.get(f"{class_name}Chunks").data.delete_many(
            where=Filter.by_property("document_uuid").equal(document_uuid)
        )
    except Exception as e:
        output["status"] = False
        output["error"] = f"[document_deleter.delete_document_helper] Error deleting document: {e}"
    return output


def delete_chat_history_document_helper(executor, class_name: str, document_uuid):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete the document
        r = c.collections.get(class_name).data.delete_by_id(document_uuid)
        # Delete the chunks of the document
        r = c.collections.get(f"{class_name}Chunks").data.delete_many(
            where=Filter.by_property("document_uuid").equal(document_uuid)
        )
    except Exception as e:
        output["status"] = False
        output["error"] = f"[document_deleter.delete_chat_history_document_helper] Error deleting chat history document: {e}"
    return output
