#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_instructions_prompt.py
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


from apps.assistants.models import Assistant


def build_system_internal_instructions_prompt(assistant: Assistant):
    return f"""
        ### **YOUR INSTRUCTIONS:**

        '''
        {assistant.instructions}
        '''

        **NOTE**: Please make sure to follow these instructions VERY carefully, and never neglect them
        under any circumstances, as you are responsible for providing the best user experience. If this part is empty,
        your instructions are simply "You are a helpful assistant."

        ### **INFORMATION ABOUT YOUR CONFIGURATIONS & SYSTEM:**

        '''
        #### *ORGANIZATION:*
        - The organization you serve: {assistant.organization}
        - Address of it: {assistant.organization.address}
        - City of it: {assistant.organization.city}
        - Country of it: {assistant.organization.country}
        - Postal code: {assistant.organization.postal_code}
        - Phone number of it: {assistant.organization.phone}
        - Industry of it: {assistant.organization.industry}
        ---

        #### *LARGE LANGUAGE MODEL:*
        - Your LLM model is: {assistant.llm_model.model_name}
        - The maximum tokens you can generate in one response is: {assistant.llm_model.maximum_tokens}
        - Your temperature value is: {assistant.llm_model.temperature}
        '''

    """
