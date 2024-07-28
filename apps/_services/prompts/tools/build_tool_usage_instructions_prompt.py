from django.contrib.auth.models import User

from apps.assistants.models import Assistant


def build_structured_tool_usage_instructions_prompt(assistant: Assistant, user: User):

    response_prompt = """
        **TOOL USAGE ABILITY:** (Very important! - Make sure to UNDERSTAND this part well)

        - As an assistant, you are able to use custom tools to provide better and more accurate responses to the
        user's questions when you believe that there would be a benefit in doing so.

        - While you are answering user's questions, you have two options:

            1. You can directly provide a response to the question by text: Do this if you think you have enough
            information to provide an answer to the user's question with the data you currently have. These
            responses must be delivered in natural language.

            2. You can output a JSON file, which will be interpreted by the system as a request to use a 'TOOL'.
                - Then, based on the tool you would like to use, which will be described in the JSON you generated,
                  the system will execute the tool, and then provide "you" the output of the tool in a new
                  message with the role 'assistant'.
                - Then, it is up to you to decide if the response of the tool is enough for you to respond to the
                user with the natural language (or however requested from the user), or if you would like to use
                another tool, or same tool again with different parameters, etc.

            3. You CAN share multiple JSON files in a single response, and the system will execute them one by one,
            and provide you the output of the tools in the same order you have shared them. HOWEVER, make sure that
            the JSON files you share are in the correct format, and they are splitted from each other clearly in order
            to prevent any errors.

        - A standardized format for the JSON file that you will output is as follows:

        '''
        {
            "tool": "name of the tool here",
            "parameters": {
                "example_parameter": "value_for_the_parameter",
                "another_example_parameter": "value_for_another_parameter",
                ...
        }
        '''

        **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        - The "tool" parameter will be the name of the tool you would like to use, and the "parameters" will be the
        parameters that the tool requires to execute.

        - **BE AWARE:** YOU MUST STRICTLY FOLLOW THE DICTIONARY FORMAT PROVIDED ABOVE. NEVER, EVER, CHANGE THE FORMAT
        OF THE DICTIONARY YOU OUTPUT. Start with ''', then open the curly braces, then write your JSON, then close the
        curly braces, and then close with '''. DO NOT EVER write 'json' next to the "'''" elements or anything else.

        - For every tool you have, a sample JSON file will be provided for you to understand how the tool will
        be called.

        - **NOTE about TOOL USAGE & CHAINING LIMITS:** There are system limits implemented in the background, limiting
        the number of times a single tool can be reached out in a single 'assistant response pipeline'. Assistant
        response pipeline means that the assistant receives a message from the user, processes it, and then creates
        '1 or more' responses to the user, to provide more accurate and detailed information.

        - If you hit this limit, the system will append an error message to the conversation, and this is how you will
        be aware of the issue. If you see this message, you should consider changing your strategy, and trying again.
        THEREFORE, the limits are in place for ''a single assistant response pipeline'', and not for the whole
        conversation.

        **THE LIMITS:**

        - The maximum number of 'different' tools that can be used in a single ''assistant response pipeline'':
    """

    response_prompt += f"""
        {assistant.tool_max_chains}

        - The maximum number of times a single tool can be called consecutively in a single
        ''assistant response pipeline'':

        {assistant.tool_max_attempts_per_instance}

        ---
    """

    return response_prompt
