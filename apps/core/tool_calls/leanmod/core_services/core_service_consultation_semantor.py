#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_consultation_semantor.py
#  Last Modified: 2024-11-10 17:15:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 17:15:45
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


def execute_semantor_consultation_query(user, llm_model, is_local, object_id, query, image_urls, file_urls):
    from apps.core.semantor.semantor_executor import SemantorVectorSearchExecutionManager
    try:
        xc = SemantorVectorSearchExecutionManager(user=user, llm_model=llm_model)
        consultation_output = xc.consult_semantor_by_query(
            is_local=is_local, consultation_object_id=object_id, query=query, image_urls=image_urls, file_urls=file_urls)
        logger.info(f"Semantor consultation query output: {consultation_output}")
    except Exception as e:
        logger.error(f"Error occurred while executing the function: {e}")
        error = f"Error occurred while executing the function: {str(e)}"
        return error
    return consultation_output
