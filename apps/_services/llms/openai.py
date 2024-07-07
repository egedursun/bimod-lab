from django.contrib.auth.models import User
from openai import OpenAI

from apps._services.prompts.history_builder import HistoryBuilder
from apps._services.prompts.prompt_builder import PromptBuilder
from apps.assistants.models import Assistant
from apps.llm_core.models import LLMCore
from apps.multimodal_chat.models import MultimodalChat


class ChatRoles:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


ACTIVE_RETRY_COUNT = 0

DEFAULT_ERROR_MESSAGE = "Failed to respond at the current moment. Please try again later."


def retry_mechanism(client):
    # if fails retry 3 times
    global ACTIVE_RETRY_COUNT
    if ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:
        ACTIVE_RETRY_COUNT += 1
        return client.respond()
    else:
        # Return the error message
        return DEFAULT_ERROR_MESSAGE


class InternalOpenAIClient:
    def __init__(self,
                 assistant: Assistant,
                 multimodal_chat: MultimodalChat
                 ):
        self.connection = OpenAI(
            api_key=assistant.llm_model.api_key,
        )
        self.assistant = assistant
        self.chat = multimodal_chat

    def respond(self):
        c = self.connection
        user = self.chat.user
        try:
            # Create the System Prompt
            prompt_messages = [PromptBuilder.build(
                assistant=self.assistant,
                user=user,
                role=ChatRoles.SYSTEM)]
            # Create the Chat History
            prompt_messages.extend(HistoryBuilder.build(chat=self.chat))
            # Retrieve the response
            response = c.chat.completions.create(
                model=self.assistant.llm_model.model_name,
                messages=prompt_messages,
                temperature=float(self.assistant.llm_model.temperature),
                frequency_penalty=float(self.assistant.llm_model.frequency_penalty),
                presence_penalty=float(self.assistant.llm_model.presence_penalty),
                max_tokens=int(self.assistant.llm_model.maximum_tokens),
                top_p=float(self.assistant.llm_model.top_p),
                # TODO: to be implement later
                #  stop=self.assistant.llm_model.stop_sequences
            )
            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content

        # Retry mechanism for the OpenAI API, for N times
        except Exception as e:
            final_response = retry_mechanism(client=self)
            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += f"""
                    Details about the Error:

                    {str(e)}
                """
                # Reset the retry mechanism
                global ACTIVE_RETRY_COUNT
                ACTIVE_RETRY_COUNT = 0

        return final_response



