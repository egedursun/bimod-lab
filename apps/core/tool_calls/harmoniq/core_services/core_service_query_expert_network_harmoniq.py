#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_query_expert_network_harmoniq.py
#  Last Modified: 2024-10-11 21:10:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-11 21:10:36
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

from apps.core.expert_networks.expert_network_executor import ExpertNetworkExecutor
from apps.leanmod.models import ExpertNetworkAssistantReference


logger = logging.getLogger(__name__)


def execute_expert_network_query_harmoniq(agent_id, xn_query, img_uris, f_uris):
    ref = ExpertNetworkAssistantReference.objects.filter(id=agent_id).first()
    if not ref:
        logger.error("The assistant-network reference with the given ID does not exist.")
        return "The assistant-network reference with the given ID does not exist."
    nx_obj = ref.network
    try:
        xc = ExpertNetworkExecutor(network=nx_obj)
        output = xc.consult_by_query(reference=ref, query=xn_query, image_urls=img_uris, file_urls=f_uris)
        logger.info(f"Expert network query output: {output}")
    except Exception as e:
        logger.error(f"Error occurred while executing the function: {e}")
        error = f"Error occurred while executing the function: {str(e)}"
        return error
    return output
