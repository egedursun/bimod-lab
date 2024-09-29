#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: openai_lean.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:07:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from openai import OpenAI

from apps._services.llms.helpers.helper_prompts import INSUFFICIENT_BALANCE_PROMPT, get_technical_error_log, \
    get_json_decode_error_log, embed_tool_call_in_prompt
from apps._services.llms.utils import find_json_presence, ChatRoles, DEFAULT_ERROR_MESSAGE, \
    GPT_DEFAULT_ENCODING_ENGINE, BIMOD_STREAMING_END_TAG, BIMOD_PROCESS_END, retry_mechanism, RetryCallersNames
from apps._services.prompts.history_builder import HistoryBuilder
from apps._services.prompts.prompt_builder import PromptBuilder
from apps._services.tools.tool_executor import ToolExecutor
from apps.leanmod.models import LeanAssistant
from apps.multimodal_chat.models import MultimodalLeanChat
from apps.multimodal_chat.utils import calculate_billable_cost_from_raw, send_log_message, BIMOD_NO_TAG_PLACEHOLDER


class InternalOpenAILeanClient:
    def __init__(self, assistant, multimodal_chat):
        self.connection = OpenAI(api_key=assistant.llm_model.api_key)
        self.lean_assistant: LeanAssistant = assistant
        self.chat: MultimodalLeanChat = multimodal_chat

    @staticmethod
    def get_no_scope_connection(llm_model):
        return OpenAI(api_key=llm_model.api_key)

    def respond_stream(self, latest_message, prev_tool_name=None, with_media=False, file_uris=None, image_uris=None):
        from apps.multimodal_chat.models import MultimodalLeanChatMessage
        from apps.llm_transaction.models import LLMTransaction

        send_log_message(f"""
            🤖 Lean Assistant started processing the query...
        """, chat_id=self.chat.id)

        print(f"[InternalOpenAILeanClient.respond_stream] Inside the respond_stream function...")

        c = self.connection
        user = self.chat.user

        send_log_message(
            f"""
             🛜 Connection information and metadata extraction completed.
        """, chat_id=self.chat.id)

        print(f"[InternalOpenAILeanClient.respond_stream] Responding to the user message...")

        try:
            # Create the System Prompt
            send_log_message(f"""
            🗃️ System prompt is being prepared...
                            """, chat_id=self.chat.id)

            try:
                prompt_messages = [PromptBuilder.build_leanmod(
                    chat=self.chat,
                    lean_assistant=self.lean_assistant,
                    user=user,
                    role=ChatRoles.SYSTEM)]

                send_log_message(f"""
            ⚡ System prompt preparation is completed.
                                """, chat_id=self.chat.id)

                print(f"[InternalOpenAILeanClient.respond_stream] System prompt created successfully.")

                # Create the Chat History
                send_log_message(f"""
            📜 Chat history is being prepared...
                          """, chat_id=self.chat.id)

                extended_messages, encryption_uuid = HistoryBuilder.build_leanmod(lean_chat=self.chat)
                prompt_messages.extend(extended_messages)

                send_log_message(f"""
            💥 Chat history preparation is completed.
                                """, chat_id=self.chat.id)

            except Exception as e:
                print(f"[InternalOpenAILeanClient.respond_stream] Error occurred while building the prompt: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while preparing the prompts for the process.
                """, chat_id=self.chat.id, stop_tag=BIMOD_PROCESS_END)

                return DEFAULT_ERROR_MESSAGE

            try:

                send_log_message(f"""
            📈 Transaction parameters are being inspected...
                                """, chat_id=self.chat.id)

                # Ask question to the GPT if user has enough balance
                latest_message_billable_cost = calculate_billable_cost_from_raw(
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    model=self.chat.lean_assistant.llm_model.model_name,
                    text=latest_message
                )
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Calculated the billable cost: {latest_message_billable_cost}")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Error occurred while calculating the billable cost: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while inspecting the transaction parameters.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            if latest_message_billable_cost > self.chat.organization.balance:
                send_log_message(f"""
            🚨 Organization has insufficient balance to proceed with the transaction. Cancelling the process.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                response = INSUFFICIENT_BALANCE_PROMPT
                # Still add the transactions related to the user message
                idle_response_transaction = LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.lean_assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=None,
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
                print(
                    f"[InternalOpenAILeanClient.respond_stream] User has insufficient balance, returning the response.")
                final_response = response
                return final_response

            send_log_message(f"""
            ♟️ Transaction parameters inspection is completed.
                                """, chat_id=self.chat.id)

            #######################################################################################################
            # *************************************************************************************************** #
            #######################################################################################################
            # RETRIEVE LLM RESPONSE WITH STREAMING
            #######################################################################################################

            send_log_message(f"""
            📡 Generating response in cooperation with the language model...
                                """, chat_id=self.chat.id)

            try:
                response_chunks = c.chat.completions.create(
                    model=self.lean_assistant.llm_model.model_name,
                    messages=prompt_messages,
                    temperature=float(self.lean_assistant.llm_model.temperature),
                    frequency_penalty=float(self.lean_assistant.llm_model.frequency_penalty),
                    presence_penalty=float(self.lean_assistant.llm_model.presence_penalty),
                    max_tokens=int(self.lean_assistant.llm_model.maximum_tokens),
                    top_p=float(self.lean_assistant.llm_model.top_p),
                    stream=True
                )
                print(f"[InternalOpenAILeanClient.respond_stream] Retrieved the response from the LLM.")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Error occurred while retrieving the response from the LLM: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while retrieving the response from the language model.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            send_log_message(f"""
            🧨 Response streamer is ready to process the response.
                                """, chat_id=self.chat.id)

            #######################################################################################################
            # *************************************************************************************************** #
            #######################################################################################################
            try:
                send_log_message(f"""
            ⚓ Response generation is in progress...
                                """, chat_id=self.chat.id)

                # Accumulate the response for backend processing
                accumulated_response = ""
                for element in response_chunks:
                    ############################
                    choices = element.choices
                    first_choice = choices[0]
                    delta = first_choice.delta
                    content = delta.content
                    ############################
                    if content is not None:
                        accumulated_response += content
                        send_log_message(f"""{content}""", stop_tag=BIMOD_NO_TAG_PLACEHOLDER, chat_id=self.chat.id)
                send_log_message(f"""""", stop_tag=BIMOD_STREAMING_END_TAG, chat_id=self.chat.id)

                send_log_message(f"""
            🔌 Generation iterations has been successfully accomplished.
                                """, chat_id=self.chat.id)

                send_log_message(f"""
            📦 Preparing the response...
                                """, chat_id=self.chat.id)

                # **NOTE:** now we need to use the "accumulated_response" string for the future steps
                print(f"[InternalOpenAILeanClient.respond_stream] Processed the response from the LLM.")
                print(f"[InternalOpenAILeanClient.respond_stream] Accumulated response: {accumulated_response}")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond] Error occurred while processing the response from the LLM: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while processing the response from the language model.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            send_log_message(f"""
            🕹️ Raw response stream has been successfully delivered.
            """, chat_id=self.chat.id)

            #######################################################################################################

            send_log_message(f"""
            🚀 Processing the transactional information...
            """, chat_id=self.chat.id)

            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.lean_assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=accumulated_response,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Created the transaction associated with the response.")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Error occurred while saving the transaction: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while saving the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            send_log_message(f"""
            🧲 Transactional information has been successfully processed.
            """, chat_id=self.chat.id)

            final_response = accumulated_response
            print(f"[InternalOpenAILeanClient.respond_stream] Final response: {final_response}")

        # Retry mechanism
        except Exception as e:
            final_response = retry_mechanism(client=self, latest_message=latest_message,
                                             caller=RetryCallersNames.RESPOND_STREAM)

            send_log_message(f"""
            🚨 Error occurred while processing the response. The lean assistant will attempt to retry...
                """, chat_id=self.chat.id)

            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += get_technical_error_log(error_logs=str(e))
                # Reset the retry mechanism
                global ACTIVE_RETRY_COUNT
                ACTIVE_RETRY_COUNT = 0
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Error occurred while responding to the user: {str(e)}")

        # if the final_response includes a tool usage call, execute the tool
        tool_response_list, json_parts_of_response = [], []
        if find_json_presence(final_response):

            send_log_message(f"""
            🛠️ Tool usage call detected in the response. Processing with the tool execution steps...
                                """, chat_id=self.chat.id)

            send_log_message(f"""
            🧰 Identifying the valid tool usage calls...
                                """, chat_id=self.chat.id)

            json_parts_of_response = find_json_presence(final_response)

            send_log_message(f"""
            💡️ Tool usage calls have been identified.
                                """, chat_id=self.chat.id)

            send_log_message(f"""
            🧭 Number of tool usage calls that is delivered: {len(json_parts_of_response)}
                """, chat_id=self.chat.id)

            tool_name = None
            for i, json_part in enumerate(json_parts_of_response):
                send_log_message(f"""
                🧮 Executing the tool usage call index: {i + 1} out of {len(json_parts_of_response)} ...
                                    """, chat_id=self.chat.id)

                try:
                    tool_executor = ToolExecutor(
                        assistant=self.lean_assistant,
                        chat=self.chat,
                        tool_usage_json_str=json_part
                    )
                    tool_response, tool_name, file_uris, image_uris = tool_executor.use_tool_lean()

                    send_log_message(f"""
                    🧰 Tool usage call for: '{tool_name}' has been successfully executed. Proceeding with the next actions...
                                        """, chat_id=self.chat.id)

                    if tool_name is not None:
                        prev_tool_name = tool_name

                    send_log_message(f"""
                    📦 Tool response from '{tool_name}' is being delivered to the lean assistant for further actions...
                                        """, chat_id=self.chat.id)

                    tool_response_list.append(f"""
                                    [{i}] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_response},
                                        [{i}b.] "file_uris": {file_uris},
                                        [{i}c.] "image_uris": {image_uris}
                                """)
                    print(f"[InternalOpenAILeanClient.respond_stream] Tool response received.")
                    print(f"[InternalOpenAILeanClient.respond_stream] Tool response: {tool_response}")

                    send_log_message(f"""
                    🎯 Tool response from '{tool_name}' has been successfully delivered to the lean assistant.
                                        """, chat_id=self.chat.id)

                except Exception as e:

                    send_log_message(f"""
                    🚨 Error occurred while executing the tool. Attempting to recover...
                                        """, chat_id=self.chat.id)

                    if tool_name is not None:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                                    [{i}] [FAILED] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_response},
                                        [{i}b.] "file_uris": [],
                                        [{i}c.] "image_uris": []
                                        [{i}d.] "error_logs": {str(e)}
                                """)
                        print(
                            f"[InternalOpenAILeanClient.respond_stream] Error occurred while executing the tool: {str(e)}")
                    else:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                                    [{i}] [FAILED / NO TOOL NAME] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_response},
                                        [{i}b.] "file_uris": [],
                                        [{i}c.] "image_uris": []
                                        [{i}d.] "error_logs": {str(e)}
                                """)
                        print(
                            f"[InternalOpenAILeanClient.respond_stream] Error occurred while executing the tool: {str(e)}")

                    send_log_message(f"""
                    🚨 Error logs have been delivered to the lean assistant. Proceeding with the next actions...
                                        """, chat_id=self.chat.id)

        send_log_message(f"""
            🧠 The lean assistant is inspecting the responses of the tools...
                                """, chat_id=self.chat.id)

        if tool_response_list:
            # Create the request as a multimodal chat message and add it to the chat

            send_log_message(f"""
            📦 Communication records for the tool requests are being prepared...
                                """, chat_id=self.chat.id)

            try:
                tool_request = MultimodalLeanChatMessage.objects.create(
                    multimodal_lean_chat=self.chat,
                    sender_type=ChatRoles.ASSISTANT.upper(),
                    message_text_content=embed_tool_call_in_prompt(json_parts_of_response=json_parts_of_response),
                    message_file_contents=[],
                    message_image_contents=[]
                )
                self.chat.lean_chat_messages.add(tool_request)
                self.chat.save()
                print(f"[InternalOpenAILeanClient.respond_stream] Saved the tool request.")

                # Stream the tool request to the UI
                send_log_message(f"""
                    ⚙️ Tool request records have been prepared. Proceeding with the next actions...
                """, chat_id=self.chat.id)

            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Error occurred while saving the tool request: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while recording the tool request. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            # if there is response from tool, create new chat message with the tool response and add it to the chat
            try:

                send_log_message(f"""
            📦 Communication records for the tool responses are being prepared...
                                """, chat_id=self.chat.id)

                tool_message = MultimodalLeanChatMessage.objects.create(
                    multimodal_lean_chat=self.chat,
                    sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                    message_text_content=str(tool_response_list),
                    message_file_contents=file_uris,
                    message_image_contents=image_uris
                )
                self.chat.lean_chat_messages.add(tool_message)
                self.chat.save()
                print(f"[InternalOpenAILeanClient.respond_stream] Saved the tool response.")

                # Stream the tool response to the UI
                send_log_message(f"""
                    ⚙️ Tool response records have been prepared. Proceeding with the next actions...
                """, chat_id=self.chat.id)

            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Error occurred while saving the tool response: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while recording the tool response. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            send_log_message(f"""
            ✨ Communication records for the tool requests and responses have been successfully prepared.
                """, chat_id=self.chat.id)

            #######################################################################################################

            send_log_message(f"""
            📦 Transactions are being prepared for the current level of operations...
                                """, chat_id=self.chat.id)

            # Create the transaction associated with the tool response
            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.lean_assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(tool_response_list),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Created the transaction associated with the tool response.")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond_stream] Error occurred while saving the transaction: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while recording the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            send_log_message(f"""
            ❇️ Transactions have been successfully prepared for the current level of operations.
                """, chat_id=self.chat.id)

            #######################################################################################################

            send_log_message(f"""
            🚀 The lean assistant is getting prepared for the next level of operations...
                                """, chat_id=self.chat.id)

            # apply the recursive call to the self function to get another reply from the lean assistant
            print(f"[InternalOpenAILeanClient.respond_stream] Recursive call to the respond function.")
            print(f"[InternalOpenAILeanClient.respond_stream] Tool message: {tool_message}")
            return self.respond_stream(latest_message=tool_message, prev_tool_name=prev_tool_name,
                                       with_media=with_media,
                                       file_uris=file_uris, image_uris=image_uris)

        # ONLY for export lean assistants API
        if with_media:
            print(
                f"[InternalOpenAILeanClient.respond_stream] Returning the response to the user with media (export lean assistants source).")
            return final_response, file_uris, image_uris
        print(f"[InternalOpenAILeanClient.respond_stream] Returning the response to the user.")

        send_log_message(f"""
            ✅ The assistant has successfully processed the query. The response is being delivered to the user...
        """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

        #######################################################################################################
        # Return the final response
        #######################################################################################################

        # Stream the final response to the UI
        try:
            # mocked_response = st.mock_stream(final_response, stop_tag=BIMOD_PROCESS_END)
            # st.stream_message(chunks=mocked_response)
            print(f"[InternalOpenAILeanClient.respond_stream] Final response streamed to the UI.")
        except Exception as e:
            print(
                f"[InternalOpenAILeanClient.respond_stream] Error occurred while streaming the final response: {str(e)}")

        return final_response

    def respond(self, latest_message, prev_tool_name=None, with_media=False, file_uris=None, image_uris=None):
        from apps.multimodal_chat.models import MultimodalLeanChatMessage
        from apps.llm_transaction.models import LLMTransaction
        c = self.connection
        user = self.chat.user
        print(f"[InternalOpenAILeanClient.respond] Responding to the user message...")

        try:
            # Create the System Prompt
            try:
                prompt_messages = [PromptBuilder.build_leanmod(
                    chat=self.chat,
                    lean_assistant=self.lean_assistant,
                    user=user,
                    role=ChatRoles.SYSTEM)]
                print(f"[InternalOpenAILeanClient.respond] System prompt created successfully.")

                extended_messages, encryption_uuid = HistoryBuilder.build_leanmod(lean_chat=self.chat)
                prompt_messages.extend(extended_messages)
            except Exception as e:
                print(f"[InternalOpenAILeanClient.respond] Error occurred while building the prompt: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                # Ask question to the GPT if user has enough balance
                latest_message_billable_cost = calculate_billable_cost_from_raw(
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    model=self.chat.lean_assistant.llm_model.model_name,
                    text=latest_message
                )
                print(
                    f"[InternalOpenAILeanClient.respond] Calculated the billable cost: {latest_message_billable_cost}")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond] Error occurred while calculating the billable cost: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            if latest_message_billable_cost > self.chat.organization.balance:
                response = INSUFFICIENT_BALANCE_PROMPT
                # Still add the transactions related to the user message
                idle_response_transaction = LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.lean_assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=None,
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
                print(f"[InternalOpenAILeanClient.respond] User has insufficient balance, returning the response.")
                final_response = response
                return final_response

            #######################################################################################################
            # *************************************************************************************************** #
            #######################################################################################################
            # RETRIEVE LLM RESPONSE
            #######################################################################################################
            try:
                response = c.chat.completions.create(
                    model=self.lean_assistant.llm_model.model_name,
                    messages=prompt_messages,
                    temperature=float(self.lean_assistant.llm_model.temperature),
                    frequency_penalty=float(self.lean_assistant.llm_model.frequency_penalty),
                    presence_penalty=float(self.lean_assistant.llm_model.presence_penalty),
                    max_tokens=int(self.lean_assistant.llm_model.maximum_tokens),
                    top_p=float(self.lean_assistant.llm_model.top_p)
                )
                print(f"[InternalOpenAILeanClient.respond] Retrieved the response from the LLM.")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond] Error occurred while retrieving the response from the LLM: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                choices = response.choices
                first_choice = choices[0]
                choice_message = first_choice.message
                choice_message_content = choice_message.content
                print(f"[InternalOpenAILeanClient.respond] Processed the response from the LLM.")
            except Exception as e:
                print(
                    f"[InternalOpenAILeanClient.respond] Error occurred while processing the response from the LLM: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.lean_assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=None,
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
                print(f"[InternalOpenAILeanClient.respond] Created the transaction associated with the response.")
            except Exception as e:
                print(f"[InternalOpenAILeanClient.respond] Error occurred while saving the transaction: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            final_response = choice_message_content
            print(f"[InternalOpenAILeanClient.respond] Returning the response to the user.")

        # Retry mechanism
        except Exception as e:
            final_response = retry_mechanism(client=self, latest_message=latest_message,
                                             caller=RetryCallersNames.RESPOND)

            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += get_technical_error_log(error_logs=str(e))
                print(f"[InternalOpenAILeanClient.respond] Error occurred while responding to the user: {str(e)}")

        # if the final_response includes a tool usage call, execute the tool
        tool_response_list, json_parts_of_response = [], []
        if find_json_presence(final_response):
            json_parts_of_response = find_json_presence(final_response)
            tool_name = None
            for i, json_part in enumerate(json_parts_of_response):
                try:
                    tool_executor = ToolExecutor(
                        assistant=self.lean_assistant,
                        chat=self.chat,
                        tool_usage_json_str=json_part
                    )
                    tool_response, tool_name, file_uris, image_uris = tool_executor.use_tool_lean()
                    if tool_name is not None:
                        prev_tool_name = tool_name

                    tool_response_list.append(f"""
                            [{i}] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_response},
                                [{i}b.] "file_uris": {file_uris},
                                [{i}c.] "image_uris": {image_uris}
                        """)
                    print(f"[InternalOpenAILeanClient.respond] Tool response received.")
                    print(f"[InternalOpenAILeanClient.respond_stream] Tool response: {tool_response}")

                except Exception as e:
                    if tool_name is not None:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                            [{i}] [FAILED] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_response},
                                [{i}b.] "file_uris": [],
                                [{i}c.] "image_uris": []
                                [{i}d.] "error_logs": {str(e)}
                        """)
                        print(f"[InternalOpenAILeanClient.respond] Error occurred while executing the tool: {str(e)}")
                    else:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                            [{i}] [FAILED / NO TOOL NAME] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_response},
                                [{i}b.] "file_uris": [],
                                [{i}c.] "image_uris": []
                                [{i}d.] "error_logs": {str(e)}
                        """)
                        print(f"[InternalOpenAILeanClient.respond] Error occurred while executing the tool: {str(e)}")

        if tool_response_list:
            # Create the request as a multimodal chat message and add it to the chat
            try:
                tool_request = MultimodalLeanChatMessage.objects.create(
                    multimodal_lean_chat=self.chat,
                    sender_type=ChatRoles.ASSISTANT.upper(),
                    message_text_content=embed_tool_call_in_prompt(json_parts_of_response=json_parts_of_response),
                    message_file_contents=[],
                    message_image_contents=[]
                )
                self.chat.lean_chat_messages.add(tool_request)
                self.chat.save()
                print(f"[InternalOpenAILeanClient.respond] Saved the tool request.")
            except Exception as e:
                print(f"[InternalOpenAILeanClient.respond] Error occurred while saving the tool request: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            # if there is response from tool, create new chat message with the tool response and add it to the chat
            try:
                tool_message = MultimodalLeanChatMessage.objects.create(
                    multimodal_lean_chat=self.chat,
                    sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                    message_text_content=str(tool_response_list),
                    message_file_contents=file_uris,
                    message_image_contents=image_uris
                )
                self.chat.lean_chat_messages.add(tool_message)
                self.chat.save()
                print(f"[InternalOpenAILeanClient.respond] Tool response: {tool_response_list}")
                print(f"[InternalOpenAILeanClient.respond] Saved the tool response.")
            except Exception as e:
                print(f"[InternalOpenAILeanClient.respond] Error occurred while saving the tool response: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            # Create the transaction associated with the tool response
            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.lean_assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(tool_response_list),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )
                print(f"[InternalOpenAILeanClient.respond] Created the transaction associated with the tool response.")
            except Exception as e:
                print(f"[InternalOpenAILeanClient.respond] Error occurred while saving the transaction: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            # apply the recursive call to the self function to get another reply from the lean assistant
            print(f"[InternalOpenAILeanClient.respond] Recursive call to the respond function.")
            return self.respond(latest_message=str(tool_response_list), prev_tool_name=prev_tool_name,
                                with_media=with_media,
                                file_uris=file_uris, image_uris=image_uris)

        # ONLY for export lean assistants API
        if with_media:
            print(
                f"[InternalOpenAILeanClient.respond] Returning the response to the user with media (export lean assistants source).")
            return final_response, file_uris, image_uris
        print(f"[InternalOpenAILeanClient.respond] Returning the response to the user.")
        return final_response
