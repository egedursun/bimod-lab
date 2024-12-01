#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: codebase_decoder.py
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

from apps.core.codebase.codebase_executor import WeaviateExecutor
from apps.core.codebase.utils import KNOWLEDGE_BASE_PROVIDERS


logger = logging.getLogger(__name__)


class CodeBaseDecoder:
    @staticmethod
    def get(connection):

        if connection.provider == KNOWLEDGE_BASE_PROVIDERS["WEAVIATE"]["code"]:
            logger.info(f"Creating WeaviateExecutor for connection: {connection}")
            return WeaviateExecutor(connection)
