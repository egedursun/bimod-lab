#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: knowledge_base_decoder.py
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
#  File: knowledge_base_decoder.py
#  Last Modified: 2024-08-05 21:13:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:06:20
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.knowledge_base.document.knowledge_base_executor import WeaviateExecutor


class KnowledgeBaseSystemDecoder:
    KNOWLEDGE_BASE_PROVIDERS = {
        "WEAVIATE": {
            "code": "weaviate",
            "name": "Weaviate"
        },
    }

    @staticmethod
    def get(connection):
        if connection.provider == KnowledgeBaseSystemDecoder.KNOWLEDGE_BASE_PROVIDERS["WEAVIATE"]["code"]:
            print(f"[KnowledgeBaseSystemDecoder.get] Weaviate provider selected.")
            return WeaviateExecutor(connection)
