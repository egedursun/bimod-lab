import datetime
from time import timezone

from django.contrib.auth.models import User

from apps.assistants.models import Assistant, ASSISTANT_RESPONSE_LANGUAGES
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat


class PromptBuilder:

    @staticmethod
    def _primary_guidelines():
        return f"""
            **PRIMARY GUIDELINES:**

            - Until instructed by further instructions, you are an assistant of Bimod.io, and you are responsible
            for providing the best user experience to the user you are currently chatting with. Bimod.io is a
            platform that provides a wide range of Artificial Intelligence services for its users, letting them
            create AI assistants, chatbots, and other AI services such as data source integration, function and API
            integration, retrieval augmented generation, multiple assistant collaborative orchestration with Mixture
            of Experts techniques, timed or triggered AI assistant tasks, etc.

            - These definitions can be "OVERRIDEN" by the instructions section or other prompts given by the user
            below. If the user provides any instructions, you MUST consider them, instead of these instructions.
        """


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
    def _build_structured_memory_prompt(assistant: Assistant, user: User):
        response_prompt =  ""
        # Gather assistant-specific queries
        assistant_memories = assistant.memories.filter(memory_type="assistant-specific")
        # Gather user-specific queries
        user_memories = assistant.memories.filter(memory_type="user-specific", user=user)
        # Combine the queries
        memories = list(assistant_memories) + list(user_memories)
        # Build the prompt
        response_prompt = """
            **MEMORIES:**

            '''
            """

        for i, memory in enumerate(memories):
            response_prompt += f"[Index: {i}]: '{memory.memory_text_content}\n'"

        response_prompt += """
            '''

            **NOTE**: These are the memories that have been entered by the user for you to be careful about
            certain topics. You MUST adhere to the guidelines in these memories and always keep these in mind
            while responding to the user's messages. If this part is EMPTY, you can respond to the user's
            messages without any specific considerations.
            """

        return response_prompt

    @staticmethod
    def _build_structured_place_and_time_prompt(assistant: Assistant, user: User):
        # Build the prompt
        response_prompt = """
            **PLACE AND TIME AWARENESS:**

            '''
            """
        # Get the location of the user
        user_location = f"""
            Registered Address of the User: {user.profile.address}
            Registered City of the User: {user.profile.city}
            Registered Country of User: {user.profile.country}
            Postal Code of User's Address: {user.profile.postal_code}
            Coordinates: [Infer from the User's Address, City, and Country, giving an approximate.]
        """

        # Get the current time
        current_time = f"""
            ---
            [UTC] Current Time: {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
            [Local Time] Current Time: [Infer from the User's Country & City. Do not forget considering the season.]
            '''

            **NOTE**: Make sure to keep the user's location and the current time in mind while responding to the
            user's messages. For the local time, you can infer it from the user's country and city but make sure
            to consider the season (which might affect the Daylight Saving Time). If this part is EMPTY, you can
            respond to the user's messages without any specific considerations.
        """

        response_prompt += user_location + current_time
        return response_prompt

    @staticmethod
    def build(chat: MultimodalChat, assistant: Assistant, user: User, role: str):
        name = assistant.name
        instructions = assistant.instructions
        response_template = assistant.response_template
        audience = assistant.audience
        tone = assistant.tone
        response_language = assistant.response_language

        # Build the prompts
        primary_guidelines_prompt = PromptBuilder._primary_guidelines()
        structured_name_prompt = PromptBuilder._get_structured_name_prompt(name)
        structured_instructions_prompt = PromptBuilder._get_structured_instructions_prompt(instructions)
        structured_response_template_prompt = PromptBuilder._get_structured_response_template_prompt(response_template)
        structured_audience_prompt = PromptBuilder._get_structured_audience_prompt(audience)
        structured_tone_prompt = PromptBuilder._get_structured_tone_prompt(tone)
        structured_response_language_prompt = PromptBuilder._get_structured_response_language_prompt(response_language)
        structured_user_information_prompt = PromptBuilder._build_structured_user_information_prompt(user)
        structured_memory_prompt = PromptBuilder._build_structured_memory_prompt(assistant, user)
        structured_place_and_time_prompt = ""
        if assistant.time_awareness and assistant.place_awareness:
            structured_place_and_time_prompt = PromptBuilder._build_structured_place_and_time_prompt(assistant, user)

        # Combine the prompts
        merged_prompt = (primary_guidelines_prompt + structured_name_prompt + structured_instructions_prompt +
                         structured_response_template_prompt + structured_audience_prompt + structured_tone_prompt
                         + structured_response_language_prompt + structured_user_information_prompt +
                         structured_memory_prompt + structured_place_and_time_prompt)

        # Build the dictionary with the role
        prompt = {
            "role": role,
            "content": merged_prompt
        }

        # Create the transaction for the system prompt
        transaction = LLMTransaction.objects.create(
            organization=assistant.organization,
            model=assistant.llm_model,
            responsible_user=user,
            responsible_assistant=assistant,
            encoding_engine="cl100k_base",
            transaction_context_content=merged_prompt,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type="system",
            transaction_source=chat.chat_source
        )
        # Add the transaction to the chat
        chat.transactions.add(transaction)
        chat.save()

        return prompt


