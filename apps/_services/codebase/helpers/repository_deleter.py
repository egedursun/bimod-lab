#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: repository_deleter.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
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
#  File: repository_deleter.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:02:51
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
