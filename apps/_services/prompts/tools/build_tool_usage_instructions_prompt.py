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

        - The "tool" parameter will be the name of the tool you would like to use, and the "parameters" will be the
        parameters that the tool requires to execute.

        - **BE AWARE:** You must not put "'''" or "'''" in the JSON file you output. This is just a template
        for you to understand how the JSON file should be structured. Your output must start with "{" and end
        with "}" for the system to correctly interpret the JSON file.

        - For every tool you have, a sample JSON file will be provided for you to understand how the tool will
        be called.

    """

    return response_prompt
