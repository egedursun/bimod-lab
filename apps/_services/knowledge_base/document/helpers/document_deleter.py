#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: document_deleter.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: document_deleter.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:05:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from weaviate.classes.query import Filter


def delete_document_helper(executor, class_name: str, document_uuid):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete the document
        _ = c.collections.get(class_name).data.delete_by_id(document_uuid)
        # Delete the chunks of document
        _ = c.collections.get(f"{class_name}Chunks").data.delete_many(
            where=Filter.by_property("document_uuid").equal(document_uuid)
        )
        print(f"[document_deleter.delete_document_helper] Deleted document: {document_uuid}")
    except Exception as e:
        output["status"] = False
        output["error"] = f"[document_deleter.delete_document_helper] Error deleting document: {e}"
    return output


def delete_chat_history_document_helper(executor, class_name: str, document_uuid):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # Delete the document
        _ = c.collections.get(class_name).data.delete_by_id(document_uuid)
        # Delete the chunks of the document
        _ = c.collections.get(f"{class_name}Chunks").data.delete_many(
            where=Filter.by_property("document_uuid").equal(document_uuid)
        )
    except Exception as e:
        output["status"] = False
        output[
            "error"] = f"[document_deleter.delete_chat_history_document_helper] Error deleting chat history document: {e}"
    print(f"[document_deleter.delete_chat_history_document_helper] Deleted chat history document: {document_uuid}")
    return output
