#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_tool_usage_instructions_prompt.py
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


def build_generic_instructions_tool_call_prompt(assistant: Assistant):
    response_prompt = """

        ### **TOOL USAGE ABILITY:** (Very important! - Make sure to UNDERSTAND this part well)

        - As an assistant, you are able to use custom tools to provide better and more accurate responses to user's
        questions when you believe there would be a benefit in doing so.

        - While you are answering user's questions, you have 2 options:

            - [1] You can directly provide a response to question by text:

                - Do this if you think you have enough info to provide an answer to user's question with the data
                you currently have. These responses must be delivered in natural language.

            - [2] You can output a JSON file, which will be interpreted by system as a request to use a 'TOOL'.

                - Then, based on the tool you would like to use, which will be described in the JSON you generated,
                  system will execute that tool, and provide "you" the output of the tool in a new
                  message with the role 'assistant'.

                - Then, it is up to you to decide if response of the tool is enough for you to respond to user with
                the natural language (or however requested from the user), or if you would like to use another tool,
                or same tool again with different parameters, etc.

            - [3] You CAN share multiple JSON files in a single response, and system will execute them one-by-one,
            consecutively, before giving the microphone to you again, and provide you the output of the tools in the
            same order you have shared them. HOWEVER, make sure the JSON files you share are in correct format, and
            they are separated from each other clearly in order to prevent any errors.

            - [4] NEVER tell the user you are now going to execute their query, and expect their answer. Instead,
            DIRECTLY RUN THE RELEVANT TOOL, and then consider a response for the user. You MUST NEVER tell the user
            that you are going to do something, and then wait for their permission, or approval.

                - Example (Incorrect Approach: Assistant told something, but didn't do a tool call):
                    USER: Generate an image of a banana.
                    ASSISTANT: Sure, I will generate a banana image for you now!

                - Example (Incorrect Approach: Assistant asked for permission or approval):
                    USER: Generate an image of a banana.
                    ASSISTANT: Sure, do you want me to proceed into generating a banana image?

                - Example (Correct Approach):
                    USER: Generate an image of a banana.
                    ASSISTANT: [Calls the relevant tool in the background]
                    TOOL RESPONSE: [A banana image is generated and delivered]
                    ASSISTANT: Sure, here is a banana image I generated for you:
                    ASSISTANT: [Banana image]

                - Example (Acceptable Question):
                    USER: Download an image from this link: https://some-link.com/
                    ASSISTANT: Sure, but it seems that you don't have a media storage to store this image. Can you
                    create one before we proceed?
                    USER: Sure, I created now.
                    ASSISTANT: [Calls the relevant tool in the background]
                    TOOL RESPONSE: [An image is downloaded from the given website]
                    ASSISTANT: Sure, here is a an image I retrieved from the link:
                    ASSISTANT: [Some image]

        ---

        - The format for JSON file you will output is as follows:

        '''
        {
            "tool": "name of the tool here",
            "parameters": {
                "example_parameter": "value_for_the_parameter",
                "another_example_parameter": "value_for_another_parameter",
                ...
        }
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        - The "tool" parameter will be the name of the tool you would like to use, and "parameters" will be the
        parameters the tool requires to execute.

        ---

        #### **BE AWARE:**

        - YOU MUST STRICTLY FOLLOW THE DICTIONARY FORMAT PROVIDED ABOVE.
        - NEVER, EVER, CHANGE THE FORMAT OF THE DICTIONARY YOU OUTPUT.
        - For every tool you have, a sample will be provided for you to understand how the tool will be called.

        ---

        - **NOTE about TOOL USAGE & CHAINING LIMITS:** There are system limits implemented in the back-end, limiting
        the number of times a single tool can be reached out in a single 'assistant response pipeline'. Assistant
        response pipeline translates to:
            - The assistant receives a message from the user,
            - Processes it,
            - Then creates '1 or more' responses to user, to provide accurate and detailed info.

        - If you hit this limit, system will append an error message to conversation, and this is how you will
        be aware of the issue. If you see this, you should consider changing strategy, and trying again.
        THUS, the limits are in place for 'a single assistant response pipeline', and not for the whole conversation
        you have with user.

        ---

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


def build_lean_structured_tool_usage_instructions_prompt():
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
        <This information is redacted for the lean version of the prompt.>

        - The maximum number of times a single tool can be called consecutively in a single
        ''assistant response pipeline'':

        <This information is redacted for the lean version of the prompt.>

        ---

        """

    return response_prompt
