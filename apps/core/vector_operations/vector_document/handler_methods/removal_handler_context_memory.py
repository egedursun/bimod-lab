#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: class_deleter.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

logger = logging.getLogger(__name__)


def delete_weaviate_class_handler(executor, class_name):
    logger.info(f"Deleting class: {class_name}")
    c = executor.connect_c()

    output = {
        "status": True,
        "error": ""
    }

    try:
        _ = c.collections.delete(class_name)
        _ = c.collections.delete(f"{class_name}Chunks")

    except Exception as e:
        output["status"] = False
        output["error"] = f"Error removing classes: {e}"

    return output
