import json
from json import JSONDecodeError
import re

from openai import OpenAI

from apps._services.prompts.history_builder import HistoryBuilder
from apps._services.prompts.prompt_builder import PromptBuilder
from apps._services.tools.tool_executor import ToolExecutor
from apps.assistants.models import Assistant
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import calculate_billable_cost_from_raw


class ChatRoles:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    # TOOL = "tool"


ACTIVE_RETRY_COUNT = 0
ACTIVE_TOOL_RETRY_COUNT = 0
ACTIVE_CHAIN_SIZE = 0

DEFAULT_ERROR_MESSAGE = "Failed to respond at the current moment. Please try again later."

GPT_DEFAULT_ENCODING_ENGINE = "cl100k_base"


def retry_mechanism(client, latest_message: MultimodalChatMessage):
    # if fails retry 3 times
    global ACTIVE_RETRY_COUNT
    if ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:
        ACTIVE_RETRY_COUNT += 1
        return client.respond(latest_message=latest_message)
    else:
        # Return the error message
        return DEFAULT_ERROR_MESSAGE


def find_json_presence(response: str):
    # put a regex to find a JSON within the response string, which will be like "...{...}..."
    pattern = re.compile(r'{.*}', re.DOTALL)
    json_matches = pattern.findall(response)
    if json_matches:
        # return the matched part of the response
        return json_matches[0]
    return None


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

    def respond(self, latest_message: MultimodalChatMessage, prev_tool_name=None):
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
            latest_message_billable_cost = calculate_billable_cost_from_raw(
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                model=self.chat.assistant.llm_model.model_name,
                text=latest_message
            )
            if latest_message_billable_cost > self.chat.organization.balance:
                response = ("System Message:\n\n\n- I'm sorry, but it seems like you don't have enough balance to "
                            "continue this conversation. \n\n- Please contact your organization's administrator to "
                            "top up your balance, or if you have the necessary permissions, you can top up your "
                            "balance yourself.")
                # Still add the transactions related to the user message
                idle_response_transaction = LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=response,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )
                self.chat.transactions.add(idle_response_transaction)
                self.chat.save()

                final_response = response
                return final_response

            #######################################################################################################
            # Retrieve the response
            #######################################################################################################
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
            #######################################################################################################

            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content

            # Add the transaction of the assistant
            LLMTransaction.objects.create(
                organization=self.chat.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=choice_message_content,
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.ASSISTANT,
                transaction_source=self.chat.chat_source
            )

            final_response = choice_message_content

        # Retry mechanism for the OpenAI API, for N times
        except Exception as e:
            final_response = retry_mechanism(client=self, latest_message=latest_message)

            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += f"""

                    Technical Details about the Error:

                    If the issue persists, please contact the system administrator and deliver the error message
                    below to provide a solution to the problem as soon as possible.

                    '''

                    {str(e)}

                    '''
                """
                # Reset the retry mechanism
                global ACTIVE_RETRY_COUNT
                ACTIVE_RETRY_COUNT = 0

        # if the final_response includes a tool usage call, execute the tool
        tool_response, json_part_of_response = None, ""
        if find_json_presence(final_response) is not None:

            # check for the rate limits
            global ACTIVE_CHAIN_SIZE
            if ACTIVE_CHAIN_SIZE > self.assistant.tool_max_chains:
                idle_overflow_message = f"""
                    {final_response}

                    ---

                    System Message:

                    The maximum number of tool chains has been reached. No further tool chains can be executed.
                    If you believe you need to be able to chain more tools, please increase the limit in the assistant
                    settings.

                    The response retrieval cycle will be stopped now.

                    ---

                """
                idle_overflow_transaction = LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=idle_overflow_message,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )
                self.chat.transactions.add(idle_overflow_transaction)
                self.chat.save()

                return idle_overflow_message

            global ACTIVE_TOOL_RETRY_COUNT
            if ACTIVE_TOOL_RETRY_COUNT > self.assistant.tool_max_attempts_per_instance:
                idle_overflow_message = f"""
                    {final_response}

                    ---

                    System Message:

                    The maximum number of attempts for the tool has been reached. No further attempts can be made
                    for retrieval via this tool in this request. If you believe you need to be able to make more
                    attempts for using the same tool, please increase the limit in the assistant settings.

                    The response retrieval cycle will be stopped now.

                """
                idle_overflow_transaction = LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=idle_overflow_message,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )
                self.chat.transactions.add(idle_overflow_transaction)
                self.chat.save()

                ACTIVE_TOOL_RETRY_COUNT = 0
                return idle_overflow_message

            # increase the retry count for the tool
            ACTIVE_TOOL_RETRY_COUNT += 1

            json_part_of_response = find_json_presence(final_response)
            tool_name = None
            try:
                tool_executor = ToolExecutor(
                    assistant=self.assistant,
                    chat=self.chat,
                    tool_usage_json_str=json_part_of_response
                )
                tool_response, tool_name = tool_executor.use_tool()
                if tool_name is not None and tool_name != prev_tool_name:
                    ACTIVE_CHAIN_SIZE += 1
                    prev_tool_name = tool_name

            except Exception as e:
                if tool_name is not None:
                    tool_response = f"""
                        System Message:

                        An error occurred while decoding the JSON response provided by the AI assistant. This might be
                        related to the incorrect formatting of the response. Please make sure that the response is in the
                        correct JSON format.

                        Error Details:

                        '''
                        {str(e)}
                        '''
                    """

                    return tool_response
                else:
                    tool_response = json.dumps(final_response)
                    return tool_response

        if tool_response:
            # Create the request as a multimodal chat message and add it to the chat
            tool_request = MultimodalChatMessage.objects.create(
                multimodal_chat=self.chat,
                sender_type="ASSISTANT",
                message_text_content=final_response
            )
            self.chat.chat_messages.add(tool_request)
            self.chat.save()

            # if there is a response from the tool, create a new multimodal chat message with the tool response,
            # and add it to the chat
            tool_message = MultimodalChatMessage.objects.create(
                multimodal_chat=self.chat,
                sender_type="TOOL",
                message_text_content=tool_response
            )
            self.chat.chat_messages.add(tool_message)
            self.chat.save()

            # Create the transaction associated with the tool response
            LLMTransaction.objects.create(
                organization=self.chat.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=tool_response,
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.ASSISTANT,
                transaction_source=self.chat.chat_source
            )

            # now apply the recursive call to the self function to get another reply from the assistant
            return self.respond(latest_message=tool_message, prev_tool_name=prev_tool_name)

        # reset the active chain size
        ACTIVE_CHAIN_SIZE = 0
        return final_response



