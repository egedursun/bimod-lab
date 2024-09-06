import io
import json
import base64 as b64
import mimetypes
import os
from pathlib import Path

import boto3
import requests
from openai import OpenAI
from openai.types.beta.threads import TextContentBlock, ImageFileContentBlock

from apps._services.data_security.ner.ner_executor import NERExecutor
from apps._services.llms.helpers.helper_prompts import HELPER_ASSISTANT_PROMPTS, AssistantRunStatuses, \
    ONE_SHOT_AFFIRMATION_PROMPT, ML_AFFIRMATION_PROMPT, INSUFFICIENT_BALANCE_PROMPT, get_technical_error_log, \
    get_maximum_tool_chains_reached_log, get_maximum_tool_attempts_reached_log, get_json_decode_error_log, \
    get_number_of_files_too_high_log, EMPTY_FILE_PATH_LOG, \
    FILE_INTERPRETER_PREPARATION_ERROR_LOG, FILE_INTERPRETER_THREAD_CREATION_ERROR_LOG, \
    FILE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, get_file_interpreter_status_log, FILE_STORAGE_CLEANUP_ERROR_LOG, \
    IMAGE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, IMAGE_INTERPRETER_RESPONSE_PROCESSING_ERROR_LOG, \
    get_number_of_ml_predictions_too_high_log, ML_MODEL_NOT_FOUND_ERROR_LOG, ML_MODEL_LOADING_ERROR_LOG, \
    ML_MODEL_OPENAI_UPLOAD_ERROR_LOG, ML_MODEL_ASSISTANT_PREPARATION_ERROR_LOG, ML_MODEL_THREAD_CREATION_ERROR_LOG, \
    ML_MODEL_RESPONSE_RETRIEVAL_ERROR_LOG, get_ml_prediction_status_log, ML_MODEL_CLEANUP_ERROR_LOG, \
    get_number_of_codes_too_high_log, CODE_INTERPRETER_ASSISTANT_PREPARATION_ERROR_LOG, \
    CODE_INTERPRETER_THREAD_CREATION_ERROR_LOG, CODE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, \
    get_code_interpreter_status_log, CODE_INTERPRETER_CLEANUP_ERROR_LOG, get_image_generation_error_log, \
    get_image_modification_error_log, get_image_variation_error_log, get_statistics_analysis_error_log, \
    embed_tool_call_in_prompt, get_audio_reading_error_log, get_audio_transcription_error_log, \
    get_audio_generation_error_log, get_audio_upload_error_log
from apps._services.llms.utils import find_json_presence, generate_random_audio_filename
from apps._services.prompts.history_builder import HistoryBuilder
from apps._services.prompts.prompt_builder import PromptBuilder
from apps._services.prompts.statistics.usage_statistics_prompt import build_usage_statistics_system_prompt
from apps._services.storages.storage_executor import GENERATED_FILES_ROOT_PATH
from apps._services.tools.tool_executor import ToolExecutor
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.multimodal_chat.utils import calculate_billable_cost_from_raw, send_log_message, BIMOD_NO_TAG_PLACEHOLDER
from config.settings import MEDIA_URL, AWS_STORAGE_BUCKET_NAME


class ChatRoles:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    ###
    # Hidden Types (Internal)
    # [i] - TOOL
    ###


ACTIVE_RETRY_COUNT = 0
ACTIVE_TOOL_RETRY_COUNT = 0
ACTIVE_CHAIN_SIZE = 0

DEFAULT_ERROR_MESSAGE = "Failed to respond at the current moment. Please try again later."
GPT_DEFAULT_ENCODING_ENGINE = "cl100k_base"
CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION = 20
CONCRETE_LIMIT_ML_MODEL_PREDICTIONS = 10

DEFAULT_IMAGE_GENERATION_MODEL = "dall-e-3"
DEFAULT_IMAGE_MODIFICATION_MODEL = "dall-e-2"
DEFAULT_IMAGE_VARIATION_MODEL = "dall-e-2"
DEFAULT_IMAGE_GENERATION_N = 1
DEFAULT_IMAGE_MODIFICATION_N = 1
DEFAULT_IMAGE_VARIATION_N = 1

DEFAULT_STATISTICS_ANALYSIS_MAX_TOKENS = 4000
DEFAULT_STATISTICS_TEMPERATURE = 0.50
DEFAULT_STATISTICS_ASSISTANT_NAME_PLACEHOLDER = "Bimod Platform Usage Statistics Assistant"
DEFAULT_STATISTICS_ASSISTANT_AUDIENCE = "Standard / Bimod Application Users"
DEFAULT_STATISTICS_ASSISTANT_TONE = "Formal & Descriptive"
DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME = "Statistics Analysis & Evaluation"


BIMOD_STREAMING_END_TAG = "<[bimod_streaming_end]>"
BIMOD_PROCESS_END = "<[bimod_process_end]>"
STREAMING_WAIT_SECONDS = 0


class DefaultImageResolutionChoices:
    class Min1024Max1792:
        SQUARE = "1024x1024"
        PORTRAIT = "1024x1792"
        LANDSCAPE = "1792x1024"


class DefaultImageQualityChoices:
    STANDARD = "standard"
    HIGH_DEFINITION = "hd"


class RetryCallersNames:
    RESPOND = "respond"
    RESPOND_STREAM = "respond_stream"


class OpenAITTSVoiceNames:
    ALLOY = "alloy"  # Male Speaker: Baritone
    ECHO = "echo"  # Male Speaker: Baritone-Bass
    FABLE = "fable"  # Male Speaker: Tenor
    ONYX = "onyx"  # Male Speaker: Bass
    NOVA = "nova"  # Female Speaker: Older and Wiser
    SHIMMER = "shimmer"  # Female Speaker: Younger and Energetic


def retry_mechanism(client, latest_message, caller="respond"):
    global ACTIVE_RETRY_COUNT
    if ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:
        ACTIVE_RETRY_COUNT += 1
        if caller == RetryCallersNames.RESPOND:
            return client.respond(latest_message=latest_message)
        elif caller == RetryCallersNames.RESPOND_STREAM:
            return client.respond_stream(latest_message=latest_message)
        else:
            return DEFAULT_ERROR_MESSAGE
    else:
        return DEFAULT_ERROR_MESSAGE


class InternalOpenAIClient:
    def __init__(self, assistant, multimodal_chat):
        self.connection = OpenAI(api_key=assistant.llm_model.api_key)
        self.assistant = assistant
        self.chat = multimodal_chat

    @staticmethod
    def get_no_scope_connection(llm_model):
        return OpenAI(api_key=llm_model.api_key)

    def respond_stream(self, latest_message, prev_tool_name=None, with_media=False, file_uris=None, image_uris=None):
        from apps.multimodal_chat.models import MultimodalChatMessage
        from apps.llm_transaction.models import LLMTransaction

        send_log_message(f"""
            🤖 Assistant started processing the query...
        """, chat_id=self.chat.id)

        print(f"[InternalOpenAIClient.respond_stream] Inside the respond_stream function...")

        c = self.connection
        user = self.chat.user

        send_log_message(
            f"""
             🛜 Connection information and metadata extraction completed.
        """, chat_id=self.chat.id)

        print(f"[InternalOpenAIClient.respond_stream] Responding to the user message...")

        ner_executor, encryption_uuid = None, None
        try:
            # Create the System Prompt
            send_log_message(f"""
            🗃️ System prompt is being prepared...
                            """, chat_id=self.chat.id)

            try:
                prompt_messages = [PromptBuilder.build(
                    chat=self.chat,
                    assistant=self.assistant,
                    user=user,
                    role=ChatRoles.SYSTEM)]

                send_log_message(f"""
            ⚡ System prompt preparation is completed.
                                """, chat_id=self.chat.id)

                print(f"[InternalOpenAIClient.respond_stream] System prompt created successfully.")

                # Create the Chat History
                send_log_message(f"""
            📜 Chat history is being prepared...
                          """, chat_id=self.chat.id)

                if self.assistant.ner_integration is not None:
                    ner_executor = NERExecutor(ner_id=self.assistant.ner_integration.id)

                extended_messages, encryption_uuid = HistoryBuilder.build(chat=self.chat, ner_executor=ner_executor)
                prompt_messages.extend(extended_messages)

                send_log_message(f"""
            💥 Chat history preparation is completed.
                                """, chat_id=self.chat.id)

            except Exception as e:
                print(f"[InternalOpenAIClient.respond_stream] Error occurred while building the prompt: {str(e)}")

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
                    model=self.chat.assistant.llm_model.model_name,
                    text=latest_message
                )
                print(f"[InternalOpenAIClient.respond_stream] Calculated the billable cost: {latest_message_billable_cost}")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond_stream] Error occurred while calculating the billable cost: {str(e)}")

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
                print(f"[InternalOpenAIClient.respond_stream] User has insufficient balance, returning the response.")
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
                    model=self.assistant.llm_model.model_name,
                    messages=prompt_messages,
                    temperature=float(self.assistant.llm_model.temperature),
                    frequency_penalty=float(self.assistant.llm_model.frequency_penalty),
                    presence_penalty=float(self.assistant.llm_model.presence_penalty),
                    max_tokens=int(self.assistant.llm_model.maximum_tokens),
                    top_p=float(self.assistant.llm_model.top_p),
                    stream=True
                )
                print(f"[InternalOpenAIClient.respond_stream] Retrieved the response from the LLM.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.respond_stream] Error occurred while retrieving the response from the LLM: {str(e)}")

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
                        send_log_message(f"""{content}""", stop_tag=BIMOD_NO_TAG_PLACEHOLDER , chat_id=self.chat.id)
                send_log_message(f"""""", stop_tag=BIMOD_STREAMING_END_TAG , chat_id=self.chat.id)

                send_log_message(f"""
            🔌 Generation iterations has been successfully accomplished.
                                """, chat_id=self.chat.id)

                ####################################################################################################
                # NER INTEGRATION - DECRYPTION
                ####################################################################################################
                if ner_executor:
                    decrypted_text = ner_executor.decrypt_text(anonymized_text=accumulated_response, uuid=encryption_uuid)
                    if decrypted_text:
                        accumulated_response = decrypted_text
                ####################################################################################################
                ####################################################################################################

                send_log_message(f"""
            📦 Preparing the response...
                                """, chat_id=self.chat.id)

                # **NOTE:** now we need to use the "accumulated_response" string for the future steps
                print(f"[InternalOpenAIClient.respond_stream] Processed the response from the LLM.")
                print(f"[InternalOpenAIClient.respond_stream] Accumulated response: {accumulated_response}")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.respond] Error occurred while processing the response from the LLM: {str(e)}")

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
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
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
                print(f"[InternalOpenAIClient.respond_stream] Created the transaction associated with the response.")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond_stream] Error occurred while saving the transaction: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while saving the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            send_log_message(f"""
            🧲 Transactional information has been successfully processed.
            """, chat_id=self.chat.id)

            final_response = accumulated_response
            print(f"[InternalOpenAIClient.respond_stream] Final response: {final_response}")

        # Retry mechanism
        except Exception as e:
            final_response = retry_mechanism(client=self, latest_message=latest_message,
                                             caller=RetryCallersNames.RESPOND_STREAM)

            send_log_message(f"""
            🚨 Error occurred while processing the response. The assistant will attempt to retry...
                """, chat_id=self.chat.id)

            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += get_technical_error_log(error_logs=str(e))
                # Reset the retry mechanism
                global ACTIVE_RETRY_COUNT
                ACTIVE_RETRY_COUNT = 0
                print(f"[InternalOpenAIClient.respond_stream] Error occurred while responding to the user: {str(e)}")

        # if the final_response includes a tool usage call, execute the tool
        tool_response_list, json_parts_of_response = [], []
        if find_json_presence(final_response):

            send_log_message(f"""
            🛠️ Tool usage call detected in the response. Processing with the tool execution steps...
                                """, chat_id=self.chat.id)

            # check for the rate limits
            global ACTIVE_CHAIN_SIZE
            if ACTIVE_CHAIN_SIZE > self.assistant.tool_max_chains:
                idle_overflow_message = get_maximum_tool_chains_reached_log(final_response=final_response)

                send_log_message(f"""
            🚨 Maximum tool chain limit has been reached. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                try:
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
                    print(f"[InternalOpenAIClient.respond_stream] Saved the transaction associated with the idle overflow.")
                except Exception as e:
                    print(f"[InternalOpenAIClient.respond_stream] Error occurred while saving the transaction: {str(e)}")

                    send_log_message(f"""
            🚨 A critical error occurred while saving the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                    return idle_overflow_message

                ACTIVE_CHAIN_SIZE = 0
                return idle_overflow_message

            global ACTIVE_TOOL_RETRY_COUNT
            if ACTIVE_TOOL_RETRY_COUNT > self.assistant.tool_max_attempts_per_instance:
                idle_overflow_message = get_maximum_tool_attempts_reached_log(final_response=final_response)

                send_log_message(f"""
            🚨 Maximum same tool attempt limit has been reached. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                try:
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
                    print(f"[InternalOpenAIClient.respond_stream] Saved the transaction associated with the idle overflow.")
                except Exception as e:
                    print(f"[InternalOpenAIClient.respond_stream] Error occurred while saving the transaction: {str(e)}")

                    send_log_message(f"""
            🚨 A critical error occurred while saving the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                    return idle_overflow_message

                ACTIVE_TOOL_RETRY_COUNT = 0
                return idle_overflow_message

            # increase the retry count for tool
            ACTIVE_TOOL_RETRY_COUNT += 1

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
                        assistant=self.assistant,
                        chat=self.chat,
                        tool_usage_json_str=json_part
                    )
                    tool_response, tool_name, file_uris, image_uris = tool_executor.use_tool()

                    send_log_message(f"""
                    🧰 Tool usage call for: '{tool_name}' has been successfully executed. Proceeding with the next actions...
                                        """, chat_id=self.chat.id)

                    if tool_name is not None and tool_name != prev_tool_name:
                        ACTIVE_CHAIN_SIZE += 1
                        prev_tool_name = tool_name

                    send_log_message(f"""
                    📦 Tool response from '{tool_name}' is being delivered to the assistant for further actions...
                                        """, chat_id=self.chat.id)

                    tool_response_list.append(f"""
                                    [{i}] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_response},
                                        [{i}b.] "file_uris": {file_uris},
                                        [{i}c.] "image_uris": {image_uris}
                                """)
                    print(f"[InternalOpenAIClient.respond_stream] Tool response received.")

                    send_log_message(f"""
                    🎯 Tool response from '{tool_name}' has been successfully delivered to the assistant.
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
                        print(f"[InternalOpenAIClient.respond_stream] Error occurred while executing the tool: {str(e)}")
                    else:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                                    [{i}] [FAILED / NO TOOL NAME] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_response},
                                        [{i}b.] "file_uris": [],
                                        [{i}c.] "image_uris": []
                                        [{i}d.] "error_logs": {str(e)}
                                """)
                        print(f"[InternalOpenAIClient.respond_stream] Error occurred while executing the tool: {str(e)}")

                    send_log_message(f"""
                    🚨 Error logs have been delivered to the assistant. Proceeding with the next actions...
                                        """, chat_id=self.chat.id)

        send_log_message(f"""
            🧠 The assistant is inspecting the responses of the tools...
                                """, chat_id=self.chat.id)

        if tool_response_list:
            # Create the request as a multimodal chat message and add it to the chat

            send_log_message(f"""
            📦 Communication records for the tool requests are being prepared...
                                """, chat_id=self.chat.id)

            try:
                tool_request = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat,
                    sender_type=ChatRoles.ASSISTANT.upper(),
                    message_text_content=embed_tool_call_in_prompt(json_parts_of_response=json_parts_of_response),
                    message_file_contents=[],
                    message_image_contents=[]
                )
                self.chat.chat_messages.add(tool_request)
                self.chat.save()
                print(f"[InternalOpenAIClient.respond_stream] Saved the tool request.")

                # Stream the tool request to the UI
                send_log_message(f"""
                    ⚙️ Tool request records have been prepared. Proceeding with the next actions...
                """, chat_id=self.chat.id)

            except Exception as e:
                print(f"[InternalOpenAIClient.respond_stream] Error occurred while saving the tool request: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while recording the tool request. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            # if there is response from tool, create new chat message with the tool response and add it to the chat
            try:

                send_log_message(f"""
            📦 Communication records for the tool responses are being prepared...
                                """, chat_id=self.chat.id)

                tool_message = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat,
                    sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                    message_text_content=str(tool_response_list),
                    message_file_contents=file_uris,
                    message_image_contents=image_uris
                )
                self.chat.chat_messages.add(tool_message)
                self.chat.save()
                print(f"[InternalOpenAIClient.respond_stream] Saved the tool response.")

                # Stream the tool response to the UI
                send_log_message(f"""
                    ⚙️ Tool response records have been prepared. Proceeding with the next actions...
                """, chat_id=self.chat.id)

            except Exception as e:
                print(f"[InternalOpenAIClient.respond_stream] Error occurred while saving the tool response: {str(e)}")

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
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
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
                print(f"[InternalOpenAIClient.respond_stream] Created the transaction associated with the tool response.")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond_stream] Error occurred while saving the transaction: {str(e)}")

                send_log_message(f"""
            🚨 A critical error occurred while recording the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE

            send_log_message(f"""
            ❇️ Transactions have been successfully prepared for the current level of operations.
                """, chat_id=self.chat.id)

            #######################################################################################################

            send_log_message(f"""
            🚀 The assistant is getting prepared for the next level of operations...
                                """, chat_id=self.chat.id)

            # apply the recursive call to the self function to get another reply from the assistant
            print(f"[InternalOpenAIClient.respond_stream] Recursive call to the respond function.")
            print(f"[InternalOpenAIClient.respond_stream] Tool message: {tool_message}")
            return self.respond_stream(latest_message=tool_message, prev_tool_name=prev_tool_name, with_media=with_media,
                                file_uris=file_uris, image_uris=image_uris)

        # reset the active chain size
        ACTIVE_CHAIN_SIZE = 0
        # ONLY for export assistants API
        if with_media:
            print(
                f"[InternalOpenAIClient.respond_stream] Returning the response to the user with media (export assistants source).")
            return final_response, file_uris, image_uris
        print(f"[InternalOpenAIClient.respond_stream] Returning the response to the user.")

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
            print(f"[InternalOpenAIClient.respond_stream] Final response streamed to the UI.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.respond_stream] Error occurred while streaming the final response: {str(e)}")

        return final_response

    def respond(self, latest_message, prev_tool_name=None, with_media=False, file_uris=None, image_uris=None):
        from apps.multimodal_chat.models import MultimodalChatMessage
        from apps.llm_transaction.models import LLMTransaction
        c = self.connection
        user = self.chat.user
        print(f"[InternalOpenAIClient.respond] Responding to the user message...")

        ner_executor, encryption_uuid = None, None
        try:
            # Create the System Prompt
            try:
                prompt_messages = [PromptBuilder.build(
                    chat=self.chat,
                    assistant=self.assistant,
                    user=user,
                    role=ChatRoles.SYSTEM)]
                print(f"[InternalOpenAIClient.respond] System prompt created successfully.")

                # Create the Chat History
                if self.assistant.ner_integration is not None:
                    ner_executor = NERExecutor(ner_id=self.assistant.ner_integration.id)

                extended_messages, encryption_uuid = HistoryBuilder.build(chat=self.chat, ner_executor=ner_executor)
                prompt_messages.extend(extended_messages)
            except Exception as e:
                print(f"[InternalOpenAIClient.respond] Error occurred while building the prompt: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                # Ask question to the GPT if user has enough balance
                latest_message_billable_cost = calculate_billable_cost_from_raw(
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    model=self.chat.assistant.llm_model.model_name,
                    text=latest_message
                )
                print(f"[InternalOpenAIClient.respond] Calculated the billable cost: {latest_message_billable_cost}")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond] Error occurred while calculating the billable cost: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            if latest_message_billable_cost > self.chat.organization.balance:
                response = INSUFFICIENT_BALANCE_PROMPT
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
                print(f"[InternalOpenAIClient.respond] User has insufficient balance, returning the response.")
                final_response = response
                return final_response

            #######################################################################################################
            # *************************************************************************************************** #
            #######################################################################################################
            # RETRIEVE LLM RESPONSE
            #######################################################################################################
            try:
                response = c.chat.completions.create(
                    model=self.assistant.llm_model.model_name,
                    messages=prompt_messages,
                    temperature=float(self.assistant.llm_model.temperature),
                    frequency_penalty=float(self.assistant.llm_model.frequency_penalty),
                    presence_penalty=float(self.assistant.llm_model.presence_penalty),
                    max_tokens=int(self.assistant.llm_model.maximum_tokens),
                    top_p=float(self.assistant.llm_model.top_p)
                )
                print(f"[InternalOpenAIClient.respond] Retrieved the response from the LLM.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.respond] Error occurred while retrieving the response from the LLM: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                choices = response.choices
                first_choice = choices[0]
                choice_message = first_choice.message
                choice_message_content = choice_message.content
                print(f"[InternalOpenAIClient.respond] Processed the response from the LLM.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.respond] Error occurred while processing the response from the LLM: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            ####################################################################################################
            # NER INTEGRATION - DECRYPTION
            ####################################################################################################
            if ner_executor:
                decrypted_text = ner_executor.decrypt_text(anonymized_text=choice_message_content,
                                                           uuid=encryption_uuid)
                if decrypted_text:
                    choice_message_content = decrypted_text
            ####################################################################################################
            ####################################################################################################

            try:
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
                print(f"[InternalOpenAIClient.respond] Created the transaction associated with the response.")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond] Error occurred while saving the transaction: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            final_response = choice_message_content
            print(f"[InternalOpenAIClient.respond] Returning the response to the user.")

        # Retry mechanism
        except Exception as e:
            final_response = retry_mechanism(client=self, latest_message=latest_message,
                                             caller=RetryCallersNames.RESPOND)

            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += get_technical_error_log(error_logs=str(e))
                # Reset the retry mechanism
                global ACTIVE_RETRY_COUNT
                ACTIVE_RETRY_COUNT = 0
                print(f"[InternalOpenAIClient.respond] Error occurred while responding to the user: {str(e)}")

        # if the final_response includes a tool usage call, execute the tool
        tool_response_list, json_parts_of_response = [], []
        if find_json_presence(final_response):
            # check for the rate limits
            global ACTIVE_CHAIN_SIZE
            if ACTIVE_CHAIN_SIZE > self.assistant.tool_max_chains:
                idle_overflow_message = get_maximum_tool_chains_reached_log(final_response=final_response)

                try:
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
                    print(f"[InternalOpenAIClient.respond] Saved the transaction associated with the idle overflow.")
                except Exception as e:
                    print(f"[InternalOpenAIClient.respond] Error occurred while saving the transaction: {str(e)}")
                    return idle_overflow_message

                ACTIVE_CHAIN_SIZE = 0
                return idle_overflow_message

            global ACTIVE_TOOL_RETRY_COUNT
            if ACTIVE_TOOL_RETRY_COUNT > self.assistant.tool_max_attempts_per_instance:
                idle_overflow_message = get_maximum_tool_attempts_reached_log(final_response=final_response)

                try:
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
                    print(f"[InternalOpenAIClient.respond] Saved the transaction associated with the idle overflow.")
                except Exception as e:
                    print(f"[InternalOpenAIClient.respond] Error occurred while saving the transaction: {str(e)}")
                    return idle_overflow_message

                ACTIVE_TOOL_RETRY_COUNT = 0
                return idle_overflow_message

            # increase the retry count for tool
            ACTIVE_TOOL_RETRY_COUNT += 1

            json_parts_of_response = find_json_presence(final_response)
            tool_name = None
            for i, json_part in enumerate(json_parts_of_response):
                try:
                    tool_executor = ToolExecutor(
                        assistant=self.assistant,
                        chat=self.chat,
                        tool_usage_json_str=json_part
                    )
                    tool_response, tool_name, file_uris, image_uris = tool_executor.use_tool()
                    if tool_name is not None and tool_name != prev_tool_name:
                        ACTIVE_CHAIN_SIZE += 1
                        prev_tool_name = tool_name

                    tool_response_list.append(f"""
                            [{i}] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_response},
                                [{i}b.] "file_uris": {file_uris},
                                [{i}c.] "image_uris": {image_uris}
                        """)
                    print(f"[InternalOpenAIClient.respond] Tool response received.")
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
                        print(f"[InternalOpenAIClient.respond] Error occurred while executing the tool: {str(e)}")
                    else:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                            [{i}] [FAILED / NO TOOL NAME] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_response},
                                [{i}b.] "file_uris": [],
                                [{i}c.] "image_uris": []
                                [{i}d.] "error_logs": {str(e)}
                        """)
                        print(f"[InternalOpenAIClient.respond] Error occurred while executing the tool: {str(e)}")

        if tool_response_list:
            # Create the request as a multimodal chat message and add it to the chat
            try:
                tool_request = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat,
                    sender_type=ChatRoles.ASSISTANT.upper(),
                    message_text_content=embed_tool_call_in_prompt(json_parts_of_response=json_parts_of_response),
                    message_file_contents=[],
                    message_image_contents=[]
                )
                self.chat.chat_messages.add(tool_request)
                self.chat.save()
                print(f"[InternalOpenAIClient.respond] Saved the tool request.")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond] Error occurred while saving the tool request: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            # if there is response from tool, create new chat message with the tool response and add it to the chat
            try:
                tool_message = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat,
                    sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                    message_text_content=str(tool_response_list),
                    message_file_contents=file_uris,
                    message_image_contents=image_uris
                )
                self.chat.chat_messages.add(tool_message)
                self.chat.save()
                print(f"[InternalOpenAIClient.respond] Saved the tool response.")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond] Error occurred while saving the tool response: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            # Create the transaction associated with the tool response
            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
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
                print(f"[InternalOpenAIClient.respond] Created the transaction associated with the tool response.")
            except Exception as e:
                print(f"[InternalOpenAIClient.respond] Error occurred while saving the transaction: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            # apply the recursive call to the self function to get another reply from the assistant
            print(f"[InternalOpenAIClient.respond] Recursive call to the respond function.")
            return self.respond(latest_message=tool_message, prev_tool_name=prev_tool_name, with_media=with_media,
                                file_uris=file_uris, image_uris=image_uris)

        # reset the active chain size
        ACTIVE_CHAIN_SIZE = 0
        # ONLY for export assistants API
        if with_media:
            print(
                f"[InternalOpenAIClient.respond] Returning the response to the user with media (export assistants source).")
            return final_response, file_uris, image_uris
        print(f"[InternalOpenAIClient.respond] Returning the response to the user.")
        return final_response

    def ask_about_file(self, full_file_paths: list, query_string: str, interpretation_temperature: float):
        client = self.connection
        print(f"[InternalOpenAIClient.ask_about_file] Asking about the file(s)...")
        if len(full_file_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_files_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION), [], []

        file_contents = []
        for path in full_file_paths:
            if not path:
                return EMPTY_FILE_PATH_LOG, [], []
            try:
                # download the file from the path
                file = requests.get(path)
                file_contents.append(file.content)
                print(f"[InternalOpenAIClient.ask_about_file] File at the path '{path}' has been read successfully.")
            except FileNotFoundError:
                print(
                    f"[InternalOpenAIClient.ask_about_file] The file at the path '{path}' could not be found, skipping file...")
                continue
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.ask_about_file] An error occurred while reading the file at the path '{path}', skipping file...")
                print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                continue

        # Upload the file to OpenAI server
        file_objects = []
        for content in file_contents:
            try:
                file = client.files.create(purpose="assistants", file=content)
                print(
                    f"[InternalOpenAIClient.ask_about_file] File has been uploaded to the OpenAI server successfully.")
                file_objects.append(file)
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.ask_about_file] An error occurred while uploading the file to the OpenAI server.")
                print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                continue

        # Prepare the assistant for the file interpretation
        try:
            assistant = client.beta.assistants.create(
                name=HELPER_ASSISTANT_PROMPTS["file_interpreter"]["name"],
                description=HELPER_ASSISTANT_PROMPTS["file_interpreter"]["description"],
                model="gpt-4o", tools=[{"type": "code_interpreter"}],
                tool_resources={"code_interpreter": {"file_ids": [x.id for x in file_objects]}},
                temperature=interpretation_temperature,
            )
            print(f"[InternalOpenAIClient.ask_about_file] Assistant has been prepared for the file interpretation.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.ask_about_file] An error occurred while preparing the assistant for the file interpretation.")
            print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
            return FILE_INTERPRETER_PREPARATION_ERROR_LOG, [], []

        # Prepare the thread
        try:
            thread = client.beta.threads.create(messages=[{"role": ChatRoles.USER,
                                                           "content": (query_string + ONE_SHOT_AFFIRMATION_PROMPT)}])
            print(f"[InternalOpenAIClient.ask_about_file] Thread has been prepared for the file interpretation.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.ask_about_file] An error occurred while preparing the thread for the file interpretation.")
            print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
            return FILE_INTERPRETER_THREAD_CREATION_ERROR_LOG, [], []

        # Retrieve the response from the assistant
        try:
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
            print(f"[InternalOpenAIClient.ask_about_file] Retrieved the response from the file interpreter assistant.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.ask_about_file] An error occurred while retrieving the response from the file interpreter assistant.")
            print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
            return FILE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, [], []

        # Format and get the messages
        texts, image_download_ids, file_download_ids = [], [], []
        if run.status == AssistantRunStatuses.COMPLETED:
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == ChatRoles.ASSISTANT:
                    root_content = message.content
                    for content in root_content:
                        if isinstance(content, TextContentBlock):
                            text_content = content.text
                            texts.append(text_content.value)
                            if text_content.annotations:
                                for annotation in text_content.annotations:
                                    file_id = annotation.file_path.file_id
                                    file_download_ids.append((file_id, annotation.text))
                                # END FOR
                            # END IF
                        elif isinstance(content, ImageFileContentBlock):
                            image_content = content.image_file.file_id
                            image_download_ids.append(image_content)
                        # END IF
                    # END FOR
                # END IF
            # END FOR
        else:
            if run.status == AssistantRunStatuses.FAILED:
                print(f"[InternalOpenAIClient.ask_about_file] The file interpretation has failed.")
                messages = get_file_interpreter_status_log(status="failed")
            elif run.status == AssistantRunStatuses.INCOMPLETE:
                print(f"[InternalOpenAIClient.ask_about_file] The file interpretation is incomplete.")
                messages = get_file_interpreter_status_log(status="incomplete")
            elif run.status == AssistantRunStatuses.EXPIRED:
                print(f"[InternalOpenAIClient.ask_about_file] The file interpretation has expired.")
                messages = get_file_interpreter_status_log(status="expired")
            elif run.status == AssistantRunStatuses.CANCELLED:
                print(f"[InternalOpenAIClient.ask_about_file] The file interpretation has been cancelled.")
                messages = get_file_interpreter_status_log(status="cancelled")
            else:
                print(f"[InternalOpenAIClient.ask_about_file] The file interpretation status is unknown.")
                messages = get_file_interpreter_status_log(status="unknown")
        # END IF

        # Download the generated images and files (if any)
        downloaded_files = []
        for file_id, remote_path in file_download_ids:
            try:
                binary_content = client.files.content(file_id).read()
                downloaded_files.append((binary_content, remote_path))
                print(
                    f"[InternalOpenAIClient.ask_about_file] File with ID '{file_id}' has been downloaded successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.ask_about_file] An error occurred while downloading the file with ID '{file_id}'.")
                print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                continue
        # END FOR

        downloaded_images = []
        for image_id in image_download_ids:
            try:
                binary_content = client.files.content(image_id).read()
                downloaded_images.append(binary_content)
                print(
                    f"[InternalOpenAIClient.ask_about_file] Image with ID '{image_id}' has been downloaded successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.ask_about_file] An error occurred while downloading the image with ID '{image_id}'.")
                print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                continue
        # END FOR

        # Clean the file storage, assistant, and thread
        try:
            for file in file_objects:
                try:
                    client.files.delete(file.id)
                except Exception as e:
                    print(
                        f"[InternalOpenAIClient.ask_about_file] An error occurred while deleting the file with ID '{file.id}'.")
                    print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                    continue
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant.id)
        except Exception as e:
            print(
                f"[InternalOpenAIClient.ask_about_file] An error occurred while cleaning up the file storage, assistant, and thread.")
            print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
            return FILE_STORAGE_CLEANUP_ERROR_LOG, [], []

        # Create the transactions
        LLMTransaction.objects.create(
            organization=self.assistant.organization,
            model=self.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=texts,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=TransactionSourcesNames.GENERATION
        )
        print(f"[InternalOpenAIClient.ask_about_file] Returning the texts, downloaded files, and downloaded images.")
        return texts, downloaded_files, downloaded_images

    def ask_about_image(self, full_image_paths: list, query_string: str, interpretation_temperature: float,
                        interpretation_maximum_tokens: int):
        client = self.connection
        print(f"[InternalOpenAIClient.ask_about_image] Asking about the image(s)...")
        if len(full_image_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_files_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION)

        image_contents = []
        for path in full_image_paths:
            if not path:
                return EMPTY_FILE_PATH_LOG
            try:
                # download the file from the path
                file = requests.get(path)
                image_contents.append({"binary": file.content, "extension": path.split(".")[-1]})
                print(f"[InternalOpenAIClient.ask_about_image] Image at the path '{path}' has been read successfully.")
            except FileNotFoundError:
                print(
                    f"[InternalOpenAIClient.ask_about_image] The image at the path '{path}' could not be found, skipping image...")
                continue
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.ask_about_image] An error occurred while reading the image at the path '{path}', skipping image...")
                print(f"[InternalOpenAIClient.ask_about_image] Error Details: {str(e)}")
                continue

        # Convert binaries to base64
        image_objects = []
        for image_content in image_contents:
            binary = image_content["binary"]
            extension = image_content["extension"]
            image_base64 = b64.b64encode(binary).decode("utf-8")
            image_objects.append({"base64": image_base64, "extension": extension})
        print(f"[InternalOpenAIClient.ask_about_image] Images has been converted to base64 successfully.")

        # Prepare the thread
        messages = [
            {"role": ChatRoles.SYSTEM,
             "content": [{"type": "text", "text": HELPER_ASSISTANT_PROMPTS["image_interpreter"]["description"]}]},
            {"role": ChatRoles.USER,
             "content": [{"type": "text", "text": (query_string + ONE_SHOT_AFFIRMATION_PROMPT)}]}
        ]
        for image_object in image_objects:
            formatted_uri = f"data:image/{image_object['extension']};base64,{image_object['base64']}"
            messages[-1]["content"].append({"type": "image_url", "image_url": {"url": formatted_uri}})
        # END FOR

        try:
            response = client.chat.completions.create(
                model=HELPER_ASSISTANT_PROMPTS["image_interpreter"]["model"],
                messages=messages,
                temperature=interpretation_temperature,
                max_tokens=interpretation_maximum_tokens
            )
            print(f"[InternalOpenAIClient.ask_about_image] Retrieved the response from the image interpreter.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.ask_about_image] An error occurred on retrieving response from image interpreter.")
            print(f"[InternalOpenAIClient.ask_about_image] Error Details: {str(e)}")
            return IMAGE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG

        try:
            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content
            print(f"[InternalOpenAIClient.ask_about_image] Processed the response from image interpreter.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.ask_about_image] An error occurred on processing the response from image interpreter.")
            print(f"[InternalOpenAIClient.ask_about_image] Error Details: {str(e)}")
            return IMAGE_INTERPRETER_RESPONSE_PROCESSING_ERROR_LOG

        # Create the transactions
        LLMTransaction.objects.create(
            organization=self.assistant.organization,
            model=self.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=final_response,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=TransactionSourcesNames.GENERATION
        )
        print(f"[InternalOpenAIClient.ask_about_image] Returning the response.")
        return final_response

    def predict_with_ml_model(self, ml_model_path, input_data_urls: list, query_string: str,
                              interpretation_temperature: float = 0.25):
        client = self.connection
        print(f"[InternalOpenAIClient.predict_with_ml_model] Predicting with the machine learning model...")
        if len(input_data_urls) > CONCRETE_LIMIT_ML_MODEL_PREDICTIONS:
            return get_number_of_ml_predictions_too_high_log(max=CONCRETE_LIMIT_ML_MODEL_PREDICTIONS), [], []

        try:
            # Load the pre-trained model from s3
            model = requests.get(ml_model_path)
            loaded_ml_model = model.content
            print(f"[InternalOpenAIClient.predict_with_ml_model] The model has been loaded successfully.")
        except FileNotFoundError:
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] The model could not be found at the path '{ml_model_path}'.")
            return ML_MODEL_NOT_FOUND_ERROR_LOG, [], []
        except Exception as e:
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while loading the model at the path '{ml_model_path}'.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_LOADING_ERROR_LOG, [], []

        file_contents = []
        for path in input_data_urls:
            if not path:
                return EMPTY_FILE_PATH_LOG, [], []
            try:
                # Read from s3 by request
                file = requests.get(path)
                file_contents.append(file.content)
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] File at the path '{path}' has been read successfully.")
            except FileNotFoundError:
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] The file at the path '{path}' could not be found, skipping file...")
                continue
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while reading the file at the path '{path}', skipping file...")
                print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                continue
        # append the machine learning model to the file contents
        file_contents.append(loaded_ml_model)

        # Upload the files and the ml model to the OpenAI server
        file_objects = []
        for i, content in enumerate(file_contents):
            try:
                file = client.files.create(purpose="assistants", file=content)
                file_objects.append(file)
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] File has been uploaded to the OpenAI server successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while uploading the file to the OpenAI server.")
                print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                if i == len(file_contents) - 1:
                    return ML_MODEL_OPENAI_UPLOAD_ERROR_LOG, [], []
                continue

        # Prepare the assistant for the file interpretation
        try:
            assistant = client.beta.assistants.create(
                name=HELPER_ASSISTANT_PROMPTS["ml_model_predictor"]["name"],
                description=HELPER_ASSISTANT_PROMPTS["ml_model_predictor"]["description"],
                model="gpt-4o", tools=[{"type": "code_interpreter"}],
                tool_resources={"code_interpreter": {"file_ids": [x.id for x in file_objects]}},
                temperature=interpretation_temperature,
            )
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] Assistant has been prepared for the ML model prediction.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while preparing the assistant for the ML model prediction.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_ASSISTANT_PREPARATION_ERROR_LOG, [], []

        # Prepare the thread
        try:
            thread = client.beta.threads.create(messages=[{"role": ChatRoles.USER,
                                                           "content": (
                                                               query_string + ONE_SHOT_AFFIRMATION_PROMPT + ML_AFFIRMATION_PROMPT)}])
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] Thread has been prepared for the ML model prediction.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while preparing the thread for the ML model prediction.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_THREAD_CREATION_ERROR_LOG, [], []

        # Retrieve the response from the assistant
        try:
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] Retrieved the response from the ML model prediction assistant.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while retrieving the response from the ML model prediction assistant.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_RESPONSE_RETRIEVAL_ERROR_LOG, [], []

        # Format and get the messages
        texts, image_download_ids, file_download_ids = [], [], []
        if run.status == AssistantRunStatuses.COMPLETED:
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == ChatRoles.ASSISTANT:
                    root_content = message.content
                    for content in root_content:
                        if isinstance(content, TextContentBlock):
                            text_content = content.text
                            texts.append(text_content.value)
                            if text_content.annotations:
                                for annotation in text_content.annotations:
                                    file_id = annotation.file_path.file_id
                                    file_download_ids.append((file_id, annotation.text))
                                # END FOR
                            # END IF
                        elif isinstance(content, ImageFileContentBlock):
                            image_content = content.image_file.file_id
                            image_download_ids.append(image_content)
                        # END IF
                    # END FOR
                # END IF
            # END FOR
        else:
            if run.status == AssistantRunStatuses.FAILED:
                print(f"[InternalOpenAIClient.predict_with_ml_model] The ML model prediction has failed.")
                messages = get_ml_prediction_status_log(status="failed")
            elif run.status == AssistantRunStatuses.INCOMPLETE:
                print(f"[InternalOpenAIClient.predict_with_ml_model] The ML model prediction is incomplete.")
                messages = get_ml_prediction_status_log(status="incomplete")
            elif run.status == AssistantRunStatuses.EXPIRED:
                print(f"[InternalOpenAIClient.predict_with_ml_model] The ML model prediction has expired.")
                messages = get_ml_prediction_status_log(status="expired")
            elif run.status == AssistantRunStatuses.CANCELLED:
                print(f"[InternalOpenAIClient.predict_with_ml_model] The ML model prediction has been cancelled.")
                messages = get_ml_prediction_status_log(status="cancelled")
            else:
                print(f"[InternalOpenAIClient.predict_with_ml_model] The ML model prediction status is unknown.")
                messages = get_ml_prediction_status_log(status="unknown")
        # END IF

        # Download the generated images and files (if any)
        downloaded_files = []
        for file_id, remote_path in file_download_ids:
            try:
                binary_content = client.files.content(file_id).read()
                downloaded_files.append((binary_content, remote_path))
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] File with ID '{file_id}' has been downloaded successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while downloading the file with ID '{file_id}'.")
                print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                continue
        # END FOR

        downloaded_images = []
        for image_id in image_download_ids:
            try:
                binary_content = client.files.content(image_id).read()
                downloaded_images.append(binary_content)
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] Image with ID '{image_id}' has been downloaded successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while downloading the image with ID '{image_id}'.")
                print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                continue
        # END FOR

        # Clean the file storage, assistant, and thread
        try:
            for file in file_objects:
                try:
                    client.files.delete(file.id)
                    print(
                        f"[InternalOpenAIClient.predict_with_ml_model] File with ID '{file.id}' has been deleted successfully.")
                except Exception as e:
                    print(
                        f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while deleting the file with ID '{file.id}'.")
                    print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                    continue
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant.id)
        except Exception as e:
            print(
                f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while cleaning up the file storage, assistant, and thread.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_CLEANUP_ERROR_LOG, [], []

        # Create the transactions
        LLMTransaction.objects.create(
            organization=self.assistant.organization,
            model=self.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=texts,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=TransactionSourcesNames.GENERATION
        )
        print(
            f"[InternalOpenAIClient.predict_with_ml_model] Returning the texts, downloaded files, and downloaded images.")
        return texts, downloaded_files, downloaded_images

    def interpret_code(self, full_file_paths: list, query_string: str, interpretation_temperature: float):
        client = self.connection
        print(f"[InternalOpenAIClient.interpret_code] Interpreting the code...")
        if len(full_file_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_codes_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION), [], []

        file_contents = []
        for path in full_file_paths:
            if not path:
                return EMPTY_FILE_PATH_LOG, [], []
            if not path.startswith("http"):
                path = f"{MEDIA_URL}{path}"
            try:
                # download the file from the path
                file = requests.get(path)
                file_contents.append(file.content)
                print(f"[InternalOpenAIClient.interpret_code] File at the path '{path}' has been read successfully.")
            except FileNotFoundError:
                print(
                    f"[InternalOpenAIClient.interpret_code] The file at the path '{path}' could not be found, skipping file...")
                continue
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.interpret_code] An error occurred while reading the file at the path '{path}', skipping file...")
                print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                continue

        # Upload the content to OpenAI server
        file_objects = []
        for content in file_contents:
            try:
                file = client.files.create(purpose="assistants", file=content)
                file_objects.append(file)
                print(
                    f"[InternalOpenAIClient.interpret_code] File has been uploaded to the OpenAI server successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.interpret_code] An error occurred while uploading the file to the OpenAI server.")
                print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                continue

        # Prepare the assistant for the code interpretation
        try:
            assistant = client.beta.assistants.create(
                name=HELPER_ASSISTANT_PROMPTS["code_interpreter"]["name"],
                description=HELPER_ASSISTANT_PROMPTS["code_interpreter"]["description"],
                model="gpt-4o", tools=[{"type": "code_interpreter"}],
                tool_resources={"code_interpreter": {"file_ids": [x.id for x in file_objects]}},
                temperature=float(interpretation_temperature)
            )
            print(f"[InternalOpenAIClient.interpret_code] Assistant has been prepared for the code interpretation.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.interpret_code] An error occurred while preparing the assistant for the code interpretation.")
            print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
            return CODE_INTERPRETER_ASSISTANT_PREPARATION_ERROR_LOG, [], []

        # Prepare the thread
        try:
            thread = client.beta.threads.create(
                messages=[{"role": ChatRoles.USER, "content": (query_string + ONE_SHOT_AFFIRMATION_PROMPT)}])
            print(f"[InternalOpenAIClient.interpret_code] Thread has been prepared for the code interpretation.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.interpret_code] An error occurred while preparing the thread for the code interpretation.")
            print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
            return CODE_INTERPRETER_THREAD_CREATION_ERROR_LOG, [], []

        # Retrieve the response from the assistant
        try:
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
            print(f"[InternalOpenAIClient.interpret_code] Retrieved the response from the code interpreter assistant.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.interpret_code] An error occurred while retrieving the response from the code interpreter assistant.")
            print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
            return CODE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, [], []

        # Format and get the messages
        texts, image_download_ids, file_download_ids = [], [], []
        if run.status == AssistantRunStatuses.COMPLETED:
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == ChatRoles.ASSISTANT:
                    root_content = message.content
                    for content in root_content:
                        if isinstance(content, TextContentBlock):
                            text_content = content.text
                            texts.append(text_content.value)
                            if text_content.annotations:
                                for annotation in text_content.annotations:
                                    file_id = annotation.file_path.file_id
                                    file_download_ids.append((file_id, annotation.text))
                                # END FOR
                            # END IF
                        elif isinstance(content, ImageFileContentBlock):
                            image_content = content.image_file.file_id
                            image_download_ids.append(image_content)
                        # END IF
                    # END FOR
                # END IF
            # END FOR
        else:
            if run.status == AssistantRunStatuses.FAILED:
                print(f"[InternalOpenAIClient.interpret_code] The code interpretation has failed.")
                messages = get_code_interpreter_status_log(status="failed")
            elif run.status == AssistantRunStatuses.INCOMPLETE:
                print(f"[InternalOpenAIClient.interpret_code] The code interpretation is incomplete.")
                messages = get_code_interpreter_status_log(status="incomplete")
            elif run.status == AssistantRunStatuses.EXPIRED:
                print(f"[InternalOpenAIClient.interpret_code] The code interpretation has expired.")
                messages = get_code_interpreter_status_log(status="expired")
            elif run.status == AssistantRunStatuses.CANCELLED:
                print(f"[InternalOpenAIClient.interpret_code] The code interpretation has been cancelled.")
                messages = get_code_interpreter_status_log(status="cancelled")
            else:
                print(f"[InternalOpenAIClient.interpret_code] The code interpretation status is unknown.")
                messages = get_code_interpreter_status_log(status="unknown")
        # END IF

        # Download the generated images and files (if any)
        downloaded_files = []
        for file_id, remote_path in file_download_ids:
            try:
                binary_content = client.files.content(file_id).read()
                downloaded_files.append((binary_content, remote_path))
                print(
                    f"[InternalOpenAIClient.interpret_code] File with ID '{file_id}' has been downloaded successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.interpret_code] An error occurred while downloading the file with ID '{file_id}'.")
                print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                continue
        # END FOR

        downloaded_images = []
        for image_id in image_download_ids:
            try:
                binary_content = client.files.content(image_id).read()
                downloaded_images.append(binary_content)
                print(
                    f"[InternalOpenAIClient.interpret_code] Image with ID '{image_id}' has been downloaded successfully.")
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.interpret_code] An error occurred while downloading the image with ID '{image_id}'.")
                print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                continue
        # END FOR

        # Clean the file storage, assistant, and thread
        try:
            for file in file_objects:
                try:
                    client.files.delete(file.id)
                except Exception as e:
                    print(
                        f"[InternalOpenAIClient.interpret_code] An error occurred while deleting the file with ID '{file.id}'.")
                    print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                    continue
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant.id)
        except Exception as e:
            print(
                f"[InternalOpenAIClient.interpret_code] An error occurred while cleaning up the file storage, assistant, and thread.")
            print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
            return CODE_INTERPRETER_CLEANUP_ERROR_LOG, [], []

        # Create the transactions
        LLMTransaction.objects.create(
            organization=self.assistant.organization,
            model=self.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=texts,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=TransactionSourcesNames.GENERATION
        )
        print(f"[InternalOpenAIClient.interpret_code] Returning the texts, downloaded files, and downloaded images.")
        return texts, downloaded_files, downloaded_images

    def generate_image(self, prompt: str, image_size: str, quality: str):
        response = {"success": False, "message": "", "image_url": ""}
        image_generation_model = DEFAULT_IMAGE_GENERATION_MODEL
        print(f"[InternalOpenAIClient.generate_image] Generating the image...")

        if image_size == "SQUARE":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE
        elif image_size == "PORTRAIT":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.PORTRAIT
        elif image_size == "LANDSCAPE":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.LANDSCAPE
        else:
            # Take SQUARE as the default choice
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        if quality == "STANDARD":
            quality = DefaultImageQualityChoices.STANDARD
        elif quality == "HIGH_DEFINITION":
            quality = DefaultImageQualityChoices.HIGH_DEFINITION
        else:
            # Take STANDARD as the default choice
            quality = DefaultImageQualityChoices.STANDARD

        try:
            image_generation_response = self.connection.images.generate(
                model=image_generation_model,
                prompt=prompt,
                size=image_size,
                quality=quality,
                n=DEFAULT_IMAGE_GENERATION_N
            )
            print(f"[InternalOpenAIClient.generate_image] Image has been generated successfully.")
            image_url = image_generation_response.data[0].url
            response["success"] = True
            response["image_url"] = image_url
            return response
        except Exception as e:
            response["message"] = get_image_generation_error_log(error_logs=str(e))
            return response

    def edit_image(self, prompt: str, edit_image_uri: str, edit_image_mask_uri: str, image_size: str):
        response = {"success": False, "message": "", "image_url": ""}
        image_modification_model = DEFAULT_IMAGE_MODIFICATION_MODEL

        if image_size == "SQUARE":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE
        elif image_size == "PORTRAIT":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.PORTRAIT
        elif image_size == "LANDSCAPE":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.LANDSCAPE
        else:
            # Take SQUARE as the default choice
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        try:
            # retrieve the files from s3
            edit_image = requests.get(edit_image_uri)
            mask_image = requests.get(edit_image_mask_uri)

            edit_image_bytes = edit_image.content
            mask_image_bytes = mask_image.content

            image_modification_response = self.connection.images.edit(
                model=image_modification_model, image=edit_image_bytes, mask=mask_image_bytes,
                prompt=prompt, n=DEFAULT_IMAGE_MODIFICATION_N, size=image_size
            )
            print(f"[InternalOpenAIClient.edit_image] Image has been modified successfully.")
            image_url = image_modification_response.data[0].url
            response["success"] = True
            response["image_url"] = image_url
            return response
        except Exception as e:
            response["message"] = get_image_modification_error_log(error_logs=str(e))
            return response

    def create_image_variation(self, image_uri: str, image_size: str):
        response = {"success": False, "message": "", "image_url": ""}
        image_variation_model = DEFAULT_IMAGE_VARIATION_MODEL

        if image_size == "SQUARE":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE
        elif image_size == "PORTRAIT":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.PORTRAIT
        elif image_size == "LANDSCAPE":
            image_size = DefaultImageResolutionChoices.Min1024Max1792.LANDSCAPE
        else:
            # Take SQUARE as the default choice
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        try:
            # retrieve the file from s3
            image = requests.get(image_uri)
            image_bytes = image.content
            print(f"[InternalOpenAIClient.create_image_variation] Image has been read successfully.")

            image_variation_response = self.connection.images.create_variation(
                model=image_variation_model,
                image=image_bytes,
                n=DEFAULT_IMAGE_VARIATION_N,
                size=image_size
            )
            print(f"[InternalOpenAIClient.create_image_variation] Image variation has been created successfully.")
            image_url = image_variation_response.data[0].url
            response["success"] = True
            response["image_url"] = image_url
        except Exception as e:
            response["message"] = get_image_variation_error_log(error_logs=str(e))
            return response
        return response

    @staticmethod
    def provide_analysis(llm_model, statistics):
        try:
            instructions = build_usage_statistics_system_prompt(statistics=statistics)
            lean_prompt = PromptBuilder.build_lean(
                assistant_name=DEFAULT_STATISTICS_ASSISTANT_NAME_PLACEHOLDER,
                instructions=instructions,
                audience=DEFAULT_STATISTICS_ASSISTANT_AUDIENCE,
                tone=DEFAULT_STATISTICS_ASSISTANT_TONE,
                chat_name=DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME)
            print(f"[InternalOpenAIClient.provide_analysis] Lean prompt has been built successfully.")
            # retrieve the answer from the assistant
            c = InternalOpenAIClient.get_no_scope_connection(llm_model=llm_model)
            response = c.chat.completions.create(
                model=llm_model.model_name,
                messages=[
                    {"role": "system", "content": json.dumps(lean_prompt, indent=4, sort_keys=True, default=str)}
                ],
                temperature=DEFAULT_STATISTICS_TEMPERATURE,
                max_tokens=DEFAULT_STATISTICS_ANALYSIS_MAX_TOKENS
            )
            print(f"[InternalOpenAIClient.provide_analysis] Retrieved the response from the assistant.")
            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            response = choice_message_content
            print(f"[InternalOpenAIClient.provide_analysis] Processed the response from the assistant.")
        except Exception as e:
            response = get_statistics_analysis_error_log(error_logs=str(e))
        return response

    def audio_to_text(self, audio_uri: str):
        response = {"success": False, "message": "", "text": ""}
        # download the file from s3 bucket
        try:
            downloaded_audio = requests.get(audio_uri)

            mime_type, _ = mimetypes.guess_type(audio_uri)
            if not mime_type:
                mime_type = 'audio/mpeg'

            file_like_audio = io.BytesIO(downloaded_audio.content)
            file_like_audio.name = audio_uri.split('/')[-1]
            print(file_like_audio.name)
            print(f"[InternalOpenAIClient.audio_to_text] Audio has been read successfully.")
        except Exception as e:
            response["message"] = get_audio_reading_error_log(error_logs=str(e))
            print(f"[InternalOpenAIClient.audio_to_text] An error occurred while reading the audio.")
            return response

        try:
            model_name = "whisper-1"
            transcription = self.connection.audio.transcriptions.create(
                model=model_name,
                file=file_like_audio,
            )
            print(f"[InternalOpenAIClient.audio_to_text] Audio has been transcribed successfully.")
            response["success"] = True
            response["text"] = transcription.text
        except Exception as e:
            response["message"] = get_audio_transcription_error_log(error_logs=str(e))
            print(f"[InternalOpenAIClient.audio_to_text] An error occurred while transcribing the audio.")
            return response

        print(f"[InternalOpenAIClient.audio_to_text] Returning the transcribed text.")
        return response

    def text_to_audio_message(self, message, extension="mp3", voice=OpenAITTSVoiceNames.ONYX):
        response = {"success": False, "message": "", "audio_url": ""}
        message_text = message.message_text_content

        try:
            model_name = "tts-1"
            output_file_name = generate_random_audio_filename(extension=extension)
            s3_path = f"{GENERATED_FILES_ROOT_PATH}{output_file_name}"
            print(f"[InternalOpenAIClient.text_to_audio_message] Determined the S3 path for the audio file: {s3_path}")
            full_uri = f"{MEDIA_URL}{s3_path}"

            temp_path = os.path.join(str(Path(__file__).parent), "tmp", output_file_name)

            client_content = self.connection.audio.speech.create(
                model=model_name,
                voice=voice,
                input=message_text,
            )
            client_content.stream_to_file(temp_path)
            print(f"[InternalOpenAIClient.text_to_audio_message] Audio has been generated and streamed successfully.")

            # read the file from the temp path
            try:
                with open(temp_path, "rb") as f:
                    audio_bytes = f.read()
                    print(f"[InternalOpenAIClient.text_to_audio_message] Audio has been read successfully.")
            except Exception as e:
                response["message"] = get_audio_reading_error_log(error_logs=str(e))
                return response

            # Add the file to boto3, s3
            try:
                s3 = boto3.client('s3')
                s3.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_path, Body=audio_bytes)
                print(f"[InternalOpenAIClient.text_to_audio_message] Audio has been uploaded to the S3 successfully.")
            except Exception as e:
                response["message"] = get_audio_upload_error_log(error_logs=str(e))
                return response

        except Exception as e:
            response["message"] = get_audio_generation_error_log(error_logs=str(e))
            print(f"[InternalOpenAIClient.text_to_audio_message] An error occurred while generating the audio: {str(e)}")
            return response

        # clean the file from the temp directory
        for i in range(3):
            try:
                os.remove(temp_path)
                print(f"[InternalOpenAIClient.text_to_audio_message] Temp file has been removed successfully.")
                break
            except Exception as e:
                print(f"[InternalOpenAIClient.text_to_audio_message] An error occurred while removing the temp file.")
                print(f"[InternalOpenAIClient.text_to_audio_message] Error Details: {str(e)}")
                continue

        response["success"] = True
        response["audio_url"] = full_uri
        print(f"[InternalOpenAIClient.text_to_audio_message] Returning the audio URL: {full_uri}")
        return response

    def text_to_audio_file(self, text_content, extension="mp3", voice=OpenAITTSVoiceNames.ALLOY):
        response = {"success": False, "message": "", "audio_url": ""}

        try:
            model_name = "tts-1"
            output_file_name = generate_random_audio_filename(extension=extension)
            s3_path = f"{GENERATED_FILES_ROOT_PATH}{output_file_name}"
            print(f"[InternalOpenAIClient.text_to_audio_file] Determined the S3 path for the audio file: {s3_path}")
            full_uri = f"{MEDIA_URL}{s3_path}"

            temp_path = os.path.join(str(Path(__file__).parent), "tmp", output_file_name)

            client_content = self.connection.audio.speech.create(
                model=model_name,
                voice=voice,
                input=text_content
            )
            client_content.stream_to_file(temp_path)
            print(f"[InternalOpenAIClient.text_to_audio_file] Audio has been generated and streamed successfully.")

            # read the file from the temp path
            try:
                with open(temp_path, "rb") as f:
                    audio_bytes = f.read()
                    print(f"[InternalOpenAIClient.text_to_audio_file] Audio has been read successfully.")
            except Exception as e:
                response["message"] = get_audio_reading_error_log(error_logs=str(e))
                return response

            # Add the file to boto3, s3
            try:
                s3 = boto3.client('s3')
                s3.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_path, Body=audio_bytes)
                print(f"[InternalOpenAIClient.text_to_audio_file] Audio has been uploaded to the S3 successfully.")
            except Exception as e:
                response["message"] = get_audio_upload_error_log(error_logs=str(e))
                return response

        except Exception as e:
            response["message"] = get_audio_generation_error_log(error_logs=str(e))
            print(f"[InternalOpenAIClient.text_to_audio_file] An error occurred while generating the audio.")
            return response

        # clean the file from the temp directory
        for i in range(3):
            try:
                os.remove(temp_path)
                print(f"[InternalOpenAIClient.text_to_audio_message] Temp file has been removed successfully.")
                break
            except Exception as e:
                print(
                    f"[InternalOpenAIClient.text_to_audio_message] An error occurred while removing the temp file.")
                print(f"[InternalOpenAIClient.text_to_audio_message] Error Details: {str(e)}")
                continue

        response["success"] = True
        response["audio_url"] = full_uri
        print(f"[InternalOpenAIClient.text_to_audio_file] Returning the audio URL: {full_uri}")
        return response
