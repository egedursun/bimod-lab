from apps.leanmod.models import LeanAssistant


def build_structured_instructions_prompt_leanmod(assistant: LeanAssistant):
    return f"""
            *INSTRUCTIONS*

            '''
            {assistant.instructions}
            '''

            NOTE: Follow instructions carefully, never neglect them.

            *ADDITIONAL INFORMATION*

            '''
            ORGANIZATION:
            Your organization: {assistant.organization}
                Address: {assistant.organization.address}
                City: {assistant.organization.city}
                Country: {assistant.organization.country}
                Postal code: {assistant.organization.postal_code}
                Phone number: {assistant.organization.phone}
                Industry: {assistant.organization.industry}
            ---
            *LANGUAGE MODEL*
            LLM: {assistant.llm_model.model_name}
                Maximum output token: {assistant.llm_model.maximum_tokens}
                Temperature: {assistant.llm_model.temperature}
            '''
        """

