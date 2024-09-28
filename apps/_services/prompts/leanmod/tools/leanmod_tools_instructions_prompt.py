def build_structured_tool_usage_instructions_prompt_leanmod():
    response_prompt = """
            *TOOL USAGE*

            - As assistant, you can use tools to provide accurate responses.

            - You have 2 option:

                1. You can provide response to question: Do it if having enough data. Response is delivered in
                natural language.

                2. You can output JSON, to request using a 'TOOL'.
                    - Based on tool, system executes, and provides output in new message with role 'assistant'.
                    - It is yours to decide if response is enough, or if need to use tools again.

            - Format of tool call:

            '''
            {
                "tool": "name here",
                "parameters": {
                    "param1": "value1",
                    "param2": "value2",
                    ...
            }
            '''

            - DO NOT WRITE 'json' in the dict or next ''' elements.
            - "tool" is name of tool you need to use.
            - "parameters" are parameters tool requires.
            - For each tool, sample is provided showing how its called.
        """
    return response_prompt
