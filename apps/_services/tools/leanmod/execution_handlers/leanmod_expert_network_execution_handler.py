#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: leanmod_expert_network_execution_handler.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps._services.expert_networks.expert_network_executor import ExpertNetworkExecutor
from apps.leanmod.models import ExpertNetworkAssistantReference


def execute_expert_network_query(assistant_id, query, image_urls, file_urls):
    network_assistant_reference = ExpertNetworkAssistantReference.objects.filter(id=assistant_id).first()
    if not network_assistant_reference:
        return ("[leanmod_expert_network_execution_handler.execute_expert_network_query] The assistant-network "
                "reference with the given ID does not exist.")
    network_object = network_assistant_reference.network
    try:
        executor = ExpertNetworkExecutor(network=network_object)
        response = executor.consult_by_query(reference=network_assistant_reference, query=query, image_urls=image_urls,
                                             file_urls=file_urls)
    except Exception as e:
        error = (f"[leanmod_expert_network_execution_handler.execute_expert_network_query] Error occurred while "
                 f"executing the function: {str(e)}")
        return error
    print(f"[leanmod_expert_network_execution_handler.execute_expert_network_query] Query executed successfully.")
    return response
