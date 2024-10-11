#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: leanmod_instructions_prompt.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps.leanmod.models import LeanAssistant


def build_structured_instructions_prompt_leanmod(assistant: LeanAssistant):
    return f"""
            ---

            ### **INSTRUCTIONS**

            '''
            {assistant.instructions}
            '''

            *NOTE:*
                - Follow instructions carefully, never neglect them.

            #### **ADDITIONAL INFORMATION**

            ---

            '''
            #### *ORGANIZATION:*
            Your organization: {assistant.organization}
                Address: {assistant.organization.address}
                City: {assistant.organization.city}
                Country: {assistant.organization.country}
                Postal code: {assistant.organization.postal_code}
                Phone number: {assistant.organization.phone}
                Industry: {assistant.organization.industry}

            ---

            #### *LANGUAGE MODEL:*
            LLM: {assistant.llm_model.model_name}
                Maximum output token: {assistant.llm_model.maximum_tokens}
                Temperature: {assistant.llm_model.temperature}
            '''

            ---
        """
