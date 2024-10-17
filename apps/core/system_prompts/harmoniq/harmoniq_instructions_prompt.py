#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: harmoniq_instructions_prompt.py
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


from apps.harmoniq.models import Harmoniq


def build_structured_instructions_prompt_harmoniq(agent: Harmoniq):
    return f"""
            ---

            ### **INSTRUCTIONS**

            '''
            {agent.optional_instructions if agent.optional_instructions else "No additional instructions provided."}
            '''

            *NOTE:*
                - Follow instructions carefully, never neglect them.

            #### **ADDITIONAL INFORMATION**

            ---

            #### *LANGUAGE MODEL:*
            LLM: {agent.llm_model.model_name}
                Maximum output token: {agent.llm_model.maximum_tokens}
                Temperature: {agent.llm_model.temperature}
            '''

            ---
        """
