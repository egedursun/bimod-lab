#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_instructions_prompt.py
#  Last Modified: 2024-11-16 00:48:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:48:58
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_structured_instructions_prompt_voidforger(voidforger):
    from apps.voidforger.models import (
        VoidForger
    )

    from apps.organization.models import (
        Organization
    )

    voidforger: VoidForger

    other_organizations = voidforger.organizations.all()

    other_organizations_data = ""

    for org in other_organizations:
        org: Organization
        other_organizations_data += f"""
            - Organization: {org.name}
            - Industry: {org.industry}
        ---
        """

    return f"""
        ---

        ### **INSTRUCTIONS**

        '''
        {voidforger.additional_instructions}
        '''

        - Follow the instructions very carefully, and never neglect them.

        #### **ADDITIONAL INFORMATION**

        ---

        '''
        #### *PRIMARY ORGANIZATION:*

        Your organization: {voidforger.llm_model.organization}
            Address: {voidforger.llm_model.organization.address}
            City: {voidforger.llm_model.organization.city}
            Country: {voidforger.llm_model.organization.country}
            Postal code: {voidforger.llm_model.organization.postal_code}
            Phone number: {voidforger.llm_model.organization.phone}
            Industry: {voidforger.llm_model.organization.industry}

        - Please note that you are responsible for multiple organizations and this organization only represent the
        primary organization you are connected to in the system.

        #### *OTHER ORGANIZATIONS:*

        {other_organizations_data}

        ---

        #### *LANGUAGE MODEL:*

        LLM: {voidforger.llm_model.model_name}
            Maximum output token: {voidforger.llm_model.maximum_tokens}
            Temperature: {voidforger.llm_model.temperature}
        '''

        ---
    """
