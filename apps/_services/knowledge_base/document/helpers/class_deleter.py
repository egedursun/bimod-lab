#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: class_deleter.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:05:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def delete_weaviate_class_helper(executor, class_name):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # delete Document class
        _ = c.collections.delete(class_name)
        # delete Chunks class
        _ = c.collections.delete(f"{class_name}Chunks")
        print(
            f"[class_deleter.delete_weaviate_class_helper] Deleted Weaviate classes: {class_name} and {class_name}Chunks")
    except Exception as e:
        output["status"] = False
        output["error"] = f"[class_deleter.delete_weaviate_class_helper] Error deleting classes: {e}"
    return output


def delete_chat_history_class_helper(executor, class_name):
    c = executor.connect_c()
    output = {"status": True, "error": ""}
    try:
        # delete Context history class
        _ = c.collections.delete(class_name)
        # delete Context Chunks class
        _ = c.collections.delete(f"{class_name}Chunks")
        print(
            f"[class_deleter.delete_chat_history_class_helper] Deleted Weaviate classes: {class_name} and {class_name}Chunks")
    except Exception as e:
        output["status"] = False
        output["error"] = f"[class_deleter.delete_chat_history_class_helper] Error deleting chat history classes: {e}"
    return output
