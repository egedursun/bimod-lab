#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_query_semantor.py
#  Last Modified: 2024-11-10 17:02:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 17:02:12
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

from apps.semantor.models import SemantorConfiguration

logger = logging.getLogger(__name__)


def execute_semantor_search_query(
    user,
    llm_model,
    query
):

    from apps.core.semantor.semantor_executor import SemantorVectorSearchExecutionManager
    try:
        xc = SemantorVectorSearchExecutionManager(
            user=user,
            llm_model=llm_model
        )

        semantor_config, _ = SemantorConfiguration.objects.get_or_create(
            user=user
        )
        semantor_config: SemantorConfiguration

        if semantor_config.is_local_network_active:
            local_network_output = xc.search_assistants(
                query=query
            )

        else:
            local_network_output = {
                "info": "Local network is not active. Please activate it from the Semantor configuration."
            }

        if semantor_config.is_global_network_active:
            global_network_output = xc.search_integrations(
                query=query
            )

        else:
            global_network_output = {
                "info": "Global network is not active. Please activate it from the Semantor configuration."
            }
        logger.info(f"Semantor search query output: {local_network_output}")

    except Exception as e:

        logger.error(f"Error occurred while executing the function: {e}")
        error = f"Error occurred while executing the function: {str(e)}"
        return error

    final_output = {
        "local_network_output": local_network_output,
        "global_network_output": global_network_output
    }

    return final_output
