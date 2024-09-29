#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: codebase_decoder.py
#  Last Modified: 2024-09-06 21:45:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:03:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.codebase.codebase_executor import WeaviateExecutor


class CodeBaseDecoder:
    KNOWLEDGE_BASE_PROVIDERS = {
        "WEAVIATE": {
            "code": "weaviate",
            "name": "Weaviate"
        },
    }

    @staticmethod
    def get(connection):
        if connection.provider == CodeBaseDecoder.KNOWLEDGE_BASE_PROVIDERS["WEAVIATE"]["code"]:
            print(f"[CodeBaseDecoder.get] Weaviate provider selected.")
            return WeaviateExecutor(connection)
