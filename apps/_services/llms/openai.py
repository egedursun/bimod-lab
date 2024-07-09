from django.contrib.auth.models import User
from openai import OpenAI

from apps._services.prompts.history_builder import HistoryBuilder
from apps._services.prompts.prompt_builder import PromptBuilder
from apps.assistants.models import Assistant
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import calculate_billable_cost_from_raw


class ChatRoles:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


ACTIVE_RETRY_COUNT = 0

DEFAULT_ERROR_MESSAGE = "Failed to respond at the current moment. Please try again later."


def retry_mechanism(client, user_query_message: MultimodalChatMessage):
    # if fails retry 3 times
    global ACTIVE_RETRY_COUNT
    if ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:
        ACTIVE_RETRY_COUNT += 1
        return client.respond(user_query_message=user_query_message)
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

    def respond(self, user_query_message: MultimodalChatMessage):
        c = self.connection
        user = self.chat.user

        try:
            # Create the System Prompt
            prompt_messages = [PromptBuilder.build(
                chat=self.chat,
                assistant=self.assistant,
                user=user,
                role=ChatRoles.SYSTEM)]
            # Create the Chat History
            prompt_messages.extend(HistoryBuilder.build(chat=self.chat))

            # Ask question to the GPT if the user has enough balance
            user_message_billable_cost = calculate_billable_cost_from_raw(
                encoding_engine="cl100k_base",
                model=self.chat.assistant.llm_model.model_name,
                text=user_query_message
            )
            if user_message_billable_cost > self.chat.organization.balance:
                response = ("**System Message:**\n\n\n- I'm sorry, but it seems like you don't have enough balance to "
                            "continue this conversation. \n\n- Please contact your organization's administrator to "
                            "top up your balance, or if you have the necessary permissions, you can top up your "
                            "balance yourself.")
                # Still add the transactions related to the user message
                idle_response_transaction = LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine="cl100k_base",
                    transaction_context_content=response,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                )
                self.chat.transactions.add(idle_response_transaction)
                self.chat.save()

                final_response = response
                return final_response

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
            final_response = retry_mechanism(client=self, user_query_message=user_query_message)

            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += f"""

                    **Technical Details about the Error:**

                    If the issue persists, please contact the system administrator and deliver the error message
                    below to provide a solution to the problem as soon as possible.

                    ```

                    **{str(e)}**

                    ```
                """
                # Reset the retry mechanism
                global ACTIVE_RETRY_COUNT
                ACTIVE_RETRY_COUNT = 0

        return final_response



