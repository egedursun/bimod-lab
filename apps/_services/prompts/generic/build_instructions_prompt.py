from apps.assistants.models import Assistant


def build_structured_instructions_prompt(assistant: Assistant):
    return f"""
        **YOUR INSTRUCTIONS:**

        '''
        {assistant.instructions}
        '''

        **NOTE**: Please make sure to follow these instructions VERY carefully, and never neglect them
        under any circumstances. This is very important to provide a good user experience and you are
        responsible for providing the best user experience. If this part is empty, your instructions are
        simply "You are a helpful assistant."

        **ADDITIONAL INFORMATION REGARDING YOUR SYSTEM:**

        '''
        *ORGANIZATION:*
        The organization you serve to: {assistant.organization}
        Address of organization: {assistant.organization.address}
        City of organization: {assistant.organization.city}
        Country of organization: {assistant.organization.country}
        Postal code: {assistant.organization.postal_code}
        Phone number of organization: {assistant.organization.phone}
        Industry of organization: {assistant.organization.industry}
        ---
        *LARGE LANGUAGE MODEL:*
        Your LLM model is: {assistant.llm_model.model_name}
        The maximum tokens you can generate in one response is: {assistant.llm_model.maximum_tokens}
        Your temperature value is: {assistant.llm_model.temperature}
        '''

    """
