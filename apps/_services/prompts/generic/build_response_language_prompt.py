from apps.assistants.models import ASSISTANT_RESPONSE_LANGUAGES


def get_structured_response_language_prompt(response_language: str):
    return f"""
        **YOUR RESPONSE LANGUAGE:**

        '''
        {response_language}
        '''

        **NOTE**: This is the language that you will be using while responding to the user's messages. If this
        part is named {ASSISTANT_RESPONSE_LANGUAGES[0]}, you MUST respond in the language the user is asking
        you the questions. If this part is EMPTY, your default language to respond to the user's messages will
        be English.
    """
