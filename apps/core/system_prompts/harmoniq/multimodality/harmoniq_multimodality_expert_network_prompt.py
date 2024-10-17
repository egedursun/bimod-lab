#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: harmoniq_tools_expert_networks_query_prompt.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_expert_networks_multi_modality_prompt_harmoniq(expert_net_and_refs: dict):
    response_prompt = """

    """
    response_prompt += """
    ### **EXPERT NETWORKS**

    '''
    """

    for net_name, expert_network in expert_net_and_refs.items():
        response_prompt += f"""
                    [Network Name: {expert_network['expert_network_name']}]
                    [Network Description: {expert_network['meta_description']}]
                    """
        for agent_id, agent_reference in expert_network['assistant_references'].items():
            response_prompt += f"""
                        [Assistant ID: {agent_reference["assistant_id"]}]
                        [Assistant Name: {agent_reference["assistant_name"]}]
                        [Assistant Description: {agent_reference["context_instructions"]}]
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
