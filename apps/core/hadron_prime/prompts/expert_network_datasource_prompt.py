#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: expert_network_datasource_prompt.py
#  Last Modified: 2024-10-17 22:44:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:44:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.hadron_prime.models import HadronNode
from apps.leanmod.models import ExpertNetworkAssistantReference, ExpertNetwork


def build_hadron_prime_expert_networks_multi_modality_prompt(node: HadronNode):
    expert_networks = node.expert_networks.all()
    response_prompt = """
    ### *EXPERT NETWORKS*

    '''
    """

    for i, expert_network in enumerate(expert_networks):
        expert_network: ExpertNetwork
        response_prompt += f"""
                    [Network Name: {expert_network.name}]
                    [Network Description: {expert_network.meta_description}]
                    """
        agent_refs = expert_network.assistant_references.all()
        for j, agent_ref in enumerate(agent_refs):
            agent_ref: ExpertNetworkAssistantReference
            assistant = agent_ref.assistant
            response_prompt += f"""
                        [Assistant ID: {agent_ref.id}]
                        [Assistant Name: {assistant.name}]
                        [Assistant Description: {agent_ref.context_instructions}]
            """

    response_prompt += """
    '''

    ---

    ####**DESCRIPTION OF FIELDS:**

    - **Assistant ID:**
        - ID of the expert assistant.

    - **Assistant Name:**
        - Name of the expert assistant.

    - **Assistant Description:**
        - Description explaining specialties of expert.

    ---

    """
    return response_prompt

