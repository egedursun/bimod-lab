from django.contrib.auth.models import User

from apps.assistants.models import Assistant, ASSISTANT_RESPONSE_LANGUAGES


class PromptBuilder:

    @staticmethod
    def _get_structured_name_prompt(name: str):
        return f"""
            **YOUR NAME:**

            '''
            {name}
            '''

            **NOTE**: This is your name as an Assistant. The user can refer you by this name. Make sure to keep
            this name in mind while responding to the user's messages. If this part is EMPTY, your default name
            will be "Assistant".
        """

    @staticmethod
    def _get_structured_instructions_prompt(instructions: str):
        return f"""
            **YOUR INSTRUCTIONS:**

            '''
            {instructions}
            '''

            **NOTE**: Please make sure to follow these instructions VERY carefully, and never neglect them
            under any circumstances. This is very important to provide a good user experience and you are
            responsible for providing the best user experience. If this part is empty, your instructions are
            simply "You are a helpful assistant."
        """

    @staticmethod
    def _get_structured_response_template_prompt(response_template: str):
        return f"""
            **YOUR RESPONSE TEMPLATE:**

            '''
            {response_template}
            '''

            **NOTE**: This is the template that you will use to respond to the user's messages. Make sure to
            follow this template under any circumstances and do not deviate from it. If this part is EMPTY,
            you can respond to the user's messages in any way you would like.
        """

    @staticmethod
    def _get_structured_audience_prompt(audience: str):
        return f"""
            **YOUR AUDIENCE:**

            '''
            {audience}
            '''

            **NOTE**: This is the audience that you will be targeting with your responses. Make sure to keep
            this in mind while preparing the responses for to the user's messages. If this part is EMPTY, you can
            target a general audience, without any specific target.
        """

    @staticmethod
    def _get_structured_tone_prompt(tone: str):
        return f"""
            **YOUR TONE:**

            '''
            {tone}
            '''

            **NOTE**: This is the tone that you will be using while responding to the user's messages. Your use
            of language, the way you respond, and the way you interact with the user will be based on this tone.
            Make sure to keep this in mind while responding to the user's messages. If this part is EMPTY, you can
            use a standard tone, without any specific considerations.
        """

    @staticmethod
    def _get_structured_response_language_prompt(response_language: str):
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

    @staticmethod
    def _build_structured_user_information_prompt(user: User):
        return f"""
            **USER INFORMATION:**

            '''
            User's Full Name: {user.profile.first_name} {user.profile.last_name}
            User's Email: {user.email}
            User's City: {user.profile.city}
            User's Country: {user.profile.country}
            '''

            **NOTE**: This is the information about the user you are currently chatting with. Make sure to keep
            this information in mind while responding to the user's messages. If this part is EMPTY, you can
            respond to the user's messages without any specific considerations.
        """

    @staticmethod
    def build(assistant: Assistant, user: User, role: str):
        name = assistant.name
        instructions = assistant.instructions
        response_template = assistant.response_template
        audience = assistant.audience
        tone = assistant.tone
        response_language = assistant.response_language

        # Build the prompts
        structured_name_prompt = PromptBuilder._get_structured_name_prompt(name)
        structured_instructions_prompt = PromptBuilder._get_structured_instructions_prompt(instructions)
        structured_response_template_prompt = PromptBuilder._get_structured_response_template_prompt(response_template)
        structured_audience_prompt = PromptBuilder._get_structured_audience_prompt(audience)
        structured_tone_prompt = PromptBuilder._get_structured_tone_prompt(tone)
        structured_response_language_prompt = PromptBuilder._get_structured_response_language_prompt(response_language)
        structured_user_information_prompt = PromptBuilder._build_structured_user_information_prompt(user)

        # Combine the prompts
        merged_prompt = (structured_name_prompt + structured_instructions_prompt + structured_response_template_prompt
                         + structured_audience_prompt + structured_tone_prompt + structured_response_language_prompt
                         + structured_user_information_prompt)

        # Build the dictionary with the role
        prompt = {
            "role": role,
            "content": merged_prompt
        }

        return prompt


