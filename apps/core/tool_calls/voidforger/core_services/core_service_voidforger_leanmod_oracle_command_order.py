#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_voidforger_leanmod_oracle_command_order.py
#  Last Modified: 2024-11-16 00:36:23
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:36:24
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


def execute_voidforger_leanmod_oracle_command_order(
    object_id,
    user,
    llm_model,
    xn_query,
    img_uris,
    f_uris
):
    from apps.core.semantor.semantor_executor import SemantorVectorSearchExecutionManager

    try:
        xc = SemantorVectorSearchExecutionManager(
            user=user,
            llm_model=llm_model
        )

        output = xc.consult_leanmod_oracle_by_query(
            consultation_object_id=object_id,
            query=xn_query,
            image_urls=img_uris,
            file_urls=f_uris
        )

        logger.info(f"LeanMod Oracle command order output: {output}")

    except Exception as e:
        logger.error(f"Error occurred while executing the function: {e}")
        error = f"Error occurred while executing the function: {str(e)}"
        return error

    return output
