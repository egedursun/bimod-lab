#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: leanmod_multimodality_expert_network_prompt.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
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
#  File: leanmod_multimodality_expert_network_prompt.py
#  Last Modified: 2024-09-23 12:33:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:10:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps.leanmod.models import LeanAssistant, ExpertNetwork, ExpertNetworkAssistantReference


def build_expert_networks_multi_modality_prompt_leanmod(lean_assistant: LeanAssistant):
    # Retrieve the functions of the assistant
    expert_networks = lean_assistant.expert_networks.all()
    # Build the prompt
    response_prompt = """
                *EXPERT NETWORKS*

                '''
                """

    for i, expert_network in enumerate(expert_networks):
        expert_network: ExpertNetwork
        response_prompt += f"""
                    [Network Name: {expert_network.name}]
                    [Network Description: {expert_network.meta_description}]
                    """
        assistant_references = expert_network.assistant_references.all()
        for j, assistant_reference in enumerate(assistant_references):
            assistant_reference: ExpertNetworkAssistantReference
            assistant = assistant_reference.assistant
            response_prompt += f"""
                        [Assistant ID: {assistant_reference.id}]
                        [Assistant Name: {assistant.name}]
                        [Assistant Description: {assistant_reference.context_instructions}]
            """

    response_prompt += """
                ---

                '''
                Assistant ID: ID of the expert assistant.
                Assistant Name: Name of the expert assistant.
                Assistant Description: Description explaining specialties of expert.

                ---
                """

    return response_prompt
