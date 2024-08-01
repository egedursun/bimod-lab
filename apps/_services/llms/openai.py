import json
import base64 as b64

from openai import OpenAI
from openai.types.beta.threads import TextContentBlock, ImageFileContentBlock

from apps._services.llms.helpers.helper_prompts import HELPER_ASSISTANT_PROMPTS, AssistantRunStatuses, \
    ONE_SHOT_AFFIRMATION_PROMPT, ML_AFFIRMATION_PROMPT, INSUFFICIENT_BALANCE_PROMPT, get_technical_error_log, \
    get_maximum_tool_chains_reached_log, get_maximum_tool_attempts_reached_log, get_json_decode_error_log, \
    embed_tool_call_in_prompt, get_number_of_files_too_high_log, EMPTY_FILE_PATH_LOG, \
    FILE_INTERPRETER_PREPARATION_ERROR_LOG, FILE_INTERPRETER_THREAD_CREATION_ERROR_LOG, \
    FILE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, get_file_interpreter_status_log, FILE_STORAGE_CLEANUP_ERROR_LOG, \
    IMAGE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, IMAGE_INTERPRETER_RESPONSE_PROCESSING_ERROR_LOG, \
    get_number_of_ml_predictions_too_high_log, ML_MODEL_NOT_FOUND_ERROR_LOG, ML_MODEL_LOADING_ERROR_LOG, \
    ML_MODEL_OPENAI_UPLOAD_ERROR_LOG, ML_MODEL_ASSISTANT_PREPARATION_ERROR_LOG, ML_MODEL_THREAD_CREATION_ERROR_LOG, \
    ML_MODEL_RESPONSE_RETRIEVAL_ERROR_LOG, get_ml_prediction_status_log, ML_MODEL_CLEANUP_ERROR_LOG, \
    get_number_of_codes_too_high_log, CODE_INTERPRETER_ASSISTANT_PREPARATION_ERROR_LOG, \
    CODE_INTERPRETER_THREAD_CREATION_ERROR_LOG, CODE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG, \
    get_code_interpreter_status_log, CODE_INTERPRETER_CLEANUP_ERROR_LOG, get_image_generation_error_log, \
    get_image_modification_error_log, get_image_variation_error_log, get_statistics_analysis_error_log
from apps._services.llms.utils import find_json_presence
from apps._services.prompts.history_builder import HistoryBuilder
from apps._services.prompts.prompt_builder import PromptBuilder
from apps._services.prompts.statistics.usage_statistics_prompt import build_usage_statistics_system_prompt
from apps._services.tools.tool_executor import ToolExecutor
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.multimodal_chat.utils import calculate_billable_cost_from_raw
from config.settings import BASE_URL


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


class DefaultImageResolutionChoices:
    class Min1024Max1792:
        SQUARE = "1024x1024"
        PORTRAIT = "1024x1792"
        LANDSCAPE = "1792x1024"


class DefaultImageQualityChoices:
    STANDARD = "standard"
    HIGH_DEFINITION = "hd"


def retry_mechanism(client, latest_message):
    global ACTIVE_RETRY_COUNT
    if ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:
        ACTIVE_RETRY_COUNT += 1
        return client.respond(latest_message=latest_message)
    else:
        return DEFAULT_ERROR_MESSAGE


class InternalOpenAIClient:
    def __init__(self,assistant, multimodal_chat):
        self.connection = OpenAI(api_key=assistant.llm_model.api_key)
        self.assistant = assistant
        self.chat = multimodal_chat

    @staticmethod
    def get_no_scope_connection(llm_model):
        return OpenAI(api_key=llm_model.api_key)

    def respond(self, latest_message, prev_tool_name=None, with_media=False, file_uris=None, image_uris=None):
        from apps.multimodal_chat.models import MultimodalChatMessage
        from apps.llm_transaction.models import LLMTransaction
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

            # Ask question to the GPT if user has enough balance
            latest_message_billable_cost = calculate_billable_cost_from_raw(
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                model=self.chat.assistant.llm_model.model_name,
                text=latest_message
            )
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
                final_response = response
                return final_response

            #######################################################################################################
            # *************************************************************************************************** #
            #######################################################################################################
            # RETRIEVE LLM RESPONSE
            #######################################################################################################
            response = c.chat.completions.create(
                model=self.assistant.llm_model.model_name,
                messages=prompt_messages,
                temperature=float(self.assistant.llm_model.temperature),
                frequency_penalty=float(self.assistant.llm_model.frequency_penalty),
                presence_penalty=float(self.assistant.llm_model.presence_penalty),
                max_tokens=int(self.assistant.llm_model.maximum_tokens),
                top_p=float(self.assistant.llm_model.top_p),
            )
            #######################################################################################################
            # *************************************************************************************************** #
            #######################################################################################################

            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content

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

        # Retry mechanism
        except Exception as e:
            final_response = retry_mechanism(client=self, latest_message=latest_message)

            # Get the error message
            if final_response == DEFAULT_ERROR_MESSAGE:
                final_response += get_technical_error_log(error_logs=str(e))
                # Reset the retry mechanism
                global ACTIVE_RETRY_COUNT
                ACTIVE_RETRY_COUNT = 0

        # if the final_response includes a tool usage call, execute the tool
        tool_response_list, json_parts_of_response = [], []
        if find_json_presence(final_response):
            # check for the rate limits
            global ACTIVE_CHAIN_SIZE
            if ACTIVE_CHAIN_SIZE > self.assistant.tool_max_chains:
                idle_overflow_message = get_maximum_tool_chains_reached_log(final_response=final_response)

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

                ACTIVE_CHAIN_SIZE = 0
                return idle_overflow_message

            global ACTIVE_TOOL_RETRY_COUNT
            if ACTIVE_TOOL_RETRY_COUNT > self.assistant.tool_max_attempts_per_instance:
                idle_overflow_message = get_maximum_tool_attempts_reached_log(final_response=final_response)

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
                except Exception as e:
                    if tool_name is not None:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                            [{i}] [FAILED] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_response},
                                [{i}b.] "file_uris": [],
                                [{i}c.] "image_uris": []
                        """)
                    else:
                        tool_response = get_json_decode_error_log(error_logs=str(e))
                        tool_response_list.append(f"""
                            [{i}] [FAILED / NO TOOL NAME] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_response},
                                [{i}b.] "file_uris": [],
                                [{i}c.] "image_uris": []
                        """)

        if tool_response_list:
            # Create the request as a multimodal chat message and add it to the chat
            tool_request = MultimodalChatMessage.objects.create(
                multimodal_chat=self.chat,
                sender_type=ChatRoles.ASSISTANT.upper(),
                message_text_content=embed_tool_call_in_prompt(json_parts_of_response=json_parts_of_response),
            )
            self.chat.chat_messages.add(tool_request)
            self.chat.save()

            # if there is response from tool, create new chat message with the tool response and add it to the chat
            tool_message = MultimodalChatMessage.objects.create(
                multimodal_chat=self.chat,
                sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                message_text_content=str(tool_response_list),
                message_file_contents=file_uris,
                message_image_contents=image_uris
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
                transaction_context_content=str(tool_response_list),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.ASSISTANT,
                transaction_source=self.chat.chat_source
            )
            # apply the recursive call to the self function to get another reply from the assistant
            return self.respond(latest_message=tool_message, prev_tool_name=prev_tool_name, with_media=with_media,
                                file_uris=file_uris, image_uris=image_uris)

        # reset the active chain size
        ACTIVE_CHAIN_SIZE = 0
        # ONLY for export assistants API
        if with_media:
            file_uris = [f"{BASE_URL}/{x}" for x in file_uris] if file_uris else []
            image_uris = [f"{BASE_URL}/{x}" for x in image_uris] if image_uris else []

            return final_response, file_uris, image_uris
        return final_response

    def ask_about_file(self, full_file_paths: list, query_string: str, interpretation_temperature: float):
        client = self.connection
        if len(full_file_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_files_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION), [], []

        file_contents = []
        for path in full_file_paths:
            if not path:
                return EMPTY_FILE_PATH_LOG, [], []
            try:
                with open(path, "rb") as file: file_contents.append(file.read())
            except FileNotFoundError:
                print(f"[InternalOpenAIClient.ask_about_file] The file at the path '{path}' could not be found, skipping file...")
                continue
            except Exception as e:
                print(f"[InternalOpenAIClient.ask_about_file] An error occurred while reading the file at the path '{path}', skipping file...")
                print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                continue

        # Upload the file to OpenAI server
        file_objects = []
        for content in file_contents:
            try:
                file = client.files.create(purpose="assistants", file=content)
                file_objects.append(file)
            except Exception as e:
                print(f"[InternalOpenAIClient.ask_about_file] An error occurred while uploading the file to the OpenAI server.")
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
        except Exception as e:
            print(f"[InternalOpenAIClient.ask_about_file] An error occurred while preparing the assistant for the file interpretation.")
            print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
            return FILE_INTERPRETER_PREPARATION_ERROR_LOG, [], []

        # Prepare the thread
        try:
            thread = client.beta.threads.create(messages=[{"role": ChatRoles.USER,
                                                           "content": (query_string + ONE_SHOT_AFFIRMATION_PROMPT)}])
        except Exception as e:
            print(f"[InternalOpenAIClient.ask_about_file] An error occurred while preparing the thread for the file interpretation.")
            print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
            return FILE_INTERPRETER_THREAD_CREATION_ERROR_LOG, [], []

        # Retrieve the response from the assistant
        try:
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
        except Exception as e:
            print(f"[InternalOpenAIClient.ask_about_file] An error occurred while retrieving the response from the file interpreter assistant.")
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
                messages = get_file_interpreter_status_log(status="failed")
            elif run.status == AssistantRunStatuses.INCOMPLETE:
                messages = get_file_interpreter_status_log(status="incomplete")
            elif run.status == AssistantRunStatuses.EXPIRED:
                messages = get_file_interpreter_status_log(status="expired")
            elif run.status == AssistantRunStatuses.CANCELLED:
                messages = get_file_interpreter_status_log(status="cancelled")
            else:
                messages = get_file_interpreter_status_log(status="unknown")
        # END IF

        # Download the generated images and files (if any)
        downloaded_files = []
        for file_id, remote_path in file_download_ids:
            try:
                binary_content = client.files.content(file_id).read()
                downloaded_files.append((binary_content, remote_path))
            except Exception as e:
                print(f"[InternalOpenAIClient.ask_about_file] An error occurred while downloading the file with ID '{file_id}'.")
                print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                continue
        # END FOR

        downloaded_images = []
        for image_id in image_download_ids:
            try:
                binary_content = client.files.content(image_id).read()
                downloaded_images.append(binary_content)
            except Exception as e:
                print(f"[InternalOpenAIClient.ask_about_file] An error occurred while downloading the image with ID '{image_id}'.")
                print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                continue
        # END FOR

        # Clean the file storage, assistant, and thread
        try:
            for file in file_objects:
                try: client.files.delete(file.id)
                except Exception as e:
                    print(f"[InternalOpenAIClient.ask_about_file] An error occurred while deleting the file with ID '{file.id}'.")
                    print(f"[InternalOpenAIClient.ask_about_file] Error Details: {str(e)}")
                    continue
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant.id)
        except Exception as e:
            print(f"[InternalOpenAIClient.ask_about_file] An error occurred while cleaning up the file storage, assistant, and thread.")
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
        return texts, downloaded_files, downloaded_images

    def ask_about_image(self, full_image_paths: list, query_string: str, interpretation_temperature: float,
                        interpretation_maximum_tokens: int):
        client = self.connection
        if len(full_image_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_files_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION)

        image_contents = []
        for path in full_image_paths:
            if not path:
                return EMPTY_FILE_PATH_LOG
            try:
                with open(path, "rb") as file: image_contents.append({"binary": file.read(), "extension": path.split(".")[-1]})
            except FileNotFoundError:
                print(f"[InternalOpenAIClient.ask_about_image] The image at the path '{path}' could not be found, skipping image...")
                continue
            except Exception as e:
                print(f"[InternalOpenAIClient.ask_about_image] An error occurred while reading the image at the path '{path}', skipping image...")
                print(f"[InternalOpenAIClient.ask_about_image] Error Details: {str(e)}")
                continue

        # Convert binaries to base64
        image_objects = []
        for image_content in image_contents:
            binary = image_content["binary"]
            extension = image_content["extension"]
            image_base64 = b64.b64encode(binary).decode("utf-8")
            image_objects.append({"base64": image_base64, "extension": extension})

        # Prepare the thread
        messages = [
            {"role": ChatRoles.SYSTEM,
             "content": [{"type": "text", "text": HELPER_ASSISTANT_PROMPTS["image_interpreter"]["description"]}]},
            {"role": ChatRoles.USER, "content": [{"type": "text", "text": (query_string + ONE_SHOT_AFFIRMATION_PROMPT)}]}
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
        except Exception as e:
            print(f"[InternalOpenAIClient.ask_about_image] An error occurred on retrieving response from image interpreter.")
            print(f"[InternalOpenAIClient.ask_about_image] Error Details: {str(e)}")
            return IMAGE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG

        try:
            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content
        except Exception as e:
            print(f"[InternalOpenAIClient.ask_about_image] An error occurred on processing the response from image interpreter.")
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
        return final_response

    def predict_with_ml_model(self, ml_model_path, input_data_urls:list, query_string: str,
                              interpretation_temperature:float = 0.25):
        client = self.connection

        if len(input_data_urls) > CONCRETE_LIMIT_ML_MODEL_PREDICTIONS:
            return get_number_of_ml_predictions_too_high_log(max=CONCRETE_LIMIT_ML_MODEL_PREDICTIONS), [], []

        try:
            # Load the pre-trained model
            with open(ml_model_path, "rb") as file:
                loaded_ml_model = file.read()
        except FileNotFoundError:
            print(f"[InternalOpenAIClient.predict_with_ml_model] The model could not be found at the path '{ml_model_path}'.")
            return ML_MODEL_NOT_FOUND_ERROR_LOG, [], []
        except Exception as e:
            print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while loading the model at the path '{ml_model_path}'.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_LOADING_ERROR_LOG, [], []

        file_contents = []
        for path in input_data_urls:
            if not path:
                return EMPTY_FILE_PATH_LOG, [], []
            try:  # Read binary file contents
                with open(path, "rb") as file:
                    file_contents.append(file.read())
            except FileNotFoundError:
                print(f"[InternalOpenAIClient.predict_with_ml_model] The file at the path '{path}' could not be found, skipping file...")
                continue
            except Exception as e:
                print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while reading the file at the path '{path}', skipping file...")
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
            except Exception as e:
                print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while uploading the file to the OpenAI server.")
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
        except Exception as e:
            print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while preparing the assistant for the ML model prediction.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_ASSISTANT_PREPARATION_ERROR_LOG, [], []

        # Prepare the thread
        try:
            thread = client.beta.threads.create(messages=[{"role": ChatRoles.USER,
                                                           "content": (query_string + ONE_SHOT_AFFIRMATION_PROMPT + ML_AFFIRMATION_PROMPT)}])
        except Exception as e:
            print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while preparing the thread for the ML model prediction.")
            print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
            return ML_MODEL_THREAD_CREATION_ERROR_LOG, [], []

        # Retrieve the response from the assistant
        try:
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
        except Exception as e:
            print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while retrieving the response from the ML model prediction assistant.")
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
                messages = get_ml_prediction_status_log(status="failed")
            elif run.status == AssistantRunStatuses.INCOMPLETE:
                messages = get_ml_prediction_status_log(status="incomplete")
            elif run.status == AssistantRunStatuses.EXPIRED:
                messages = get_ml_prediction_status_log(status="expired")
            elif run.status == AssistantRunStatuses.CANCELLED:
                messages = get_ml_prediction_status_log(status="cancelled")
            else:
                messages = get_ml_prediction_status_log(status="unknown")
        # END IF

        # Download the generated images and files (if any)
        downloaded_files = []
        for file_id, remote_path in file_download_ids:
            try:
                binary_content = client.files.content(file_id).read()
                downloaded_files.append((binary_content, remote_path))
            except Exception as e:
                print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while downloading the file with ID '{file_id}'.")
                print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                continue
        # END FOR

        downloaded_images = []
        for image_id in image_download_ids:
            try:
                binary_content = client.files.content(image_id).read()
                downloaded_images.append(binary_content)
            except Exception as e:
                print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while downloading the image with ID '{image_id}'.")
                print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                continue
        # END FOR

        # Clean the file storage, assistant, and thread
        try:
            for file in file_objects:
                try:
                    client.files.delete(file.id)
                except Exception as e:
                    print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while deleting the file with ID '{file.id}'.")
                    print(f"[InternalOpenAIClient.predict_with_ml_model] Error Details: {str(e)}")
                    continue
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant.id)
        except Exception as e:
            print(f"[InternalOpenAIClient.predict_with_ml_model] An error occurred while cleaning up the file storage, assistant, and thread.")
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
        return texts, downloaded_files, downloaded_images

    def interpret_code(self, full_file_paths: list, query_string: str, interpretation_temperature: float):
        client = self.connection
        if len(full_file_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_codes_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION), [], []

        file_contents = []
        for path in full_file_paths:
            if not path:
                return EMPTY_FILE_PATH_LOG, [], []
            try:
                with open(path, "rb") as file:
                    file_contents.append(file.read())
            except FileNotFoundError:
                print(f"[InternalOpenAIClient.interpret_code] The file at the path '{path}' could not be found, skipping file...")
                continue
            except Exception as e:
                print(f"[InternalOpenAIClient.interpret_code] An error occurred while reading the file at the path '{path}', skipping file...")
                print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                continue

        # Upload the content to OpenAI server
        file_objects = []
        for content in file_contents:
            try:
                file = client.files.create(purpose="assistants", file=content)
                file_objects.append(file)
            except Exception as e:
                print(f"[InternalOpenAIClient.interpret_code] An error occurred while uploading the file to the OpenAI server.")
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
        except Exception as e:
            print(f"[InternalOpenAIClient.interpret_code] An error occurred while preparing the assistant for the code interpretation.")
            print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
            return CODE_INTERPRETER_ASSISTANT_PREPARATION_ERROR_LOG, [], []

        # Prepare the thread
        try:
            thread = client.beta.threads.create(messages=[{"role": ChatRoles.USER, "content": (query_string + ONE_SHOT_AFFIRMATION_PROMPT)}])
        except Exception as e:
            print(f"[InternalOpenAIClient.interpret_code] An error occurred while preparing the thread for the code interpretation.")
            print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
            return CODE_INTERPRETER_THREAD_CREATION_ERROR_LOG, [], []

        # Retrieve the response from the assistant
        try:
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
        except Exception as e:
            print(f"[InternalOpenAIClient.interpret_code] An error occurred while retrieving the response from the code interpreter assistant.")
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
                messages = get_code_interpreter_status_log(status="failed")
            elif run.status == AssistantRunStatuses.INCOMPLETE:
                messages = get_code_interpreter_status_log(status="incomplete")
            elif run.status == AssistantRunStatuses.EXPIRED:
                messages = get_code_interpreter_status_log(status="expired")
            elif run.status == AssistantRunStatuses.CANCELLED:
                messages = get_code_interpreter_status_log(status="cancelled")
            else:
                messages = get_code_interpreter_status_log(status="unknown")
        # END IF

        # Download the generated images and files (if any)
        downloaded_files = []
        for file_id, remote_path in file_download_ids:
            try:
                binary_content = client.files.content(file_id).read()
                downloaded_files.append((binary_content, remote_path))
            except Exception as e:
                print(f"[InternalOpenAIClient.interpret_code] An error occurred while downloading the file with ID '{file_id}'.")
                print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                continue
        # END FOR

        downloaded_images = []
        for image_id in image_download_ids:
            try:
                binary_content = client.files.content(image_id).read()
                downloaded_images.append(binary_content)
            except Exception as e:
                print(f"[InternalOpenAIClient.interpret_code] An error occurred while downloading the image with ID '{image_id}'.")
                print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                continue
        # END FOR

        # Clean the file storage, assistant, and thread
        try:
            for file in file_objects:
                try: client.files.delete(file.id)
                except Exception as e:
                    print(f"[InternalOpenAIClient.interpret_code] An error occurred while deleting the file with ID '{file.id}'.")
                    print(f"[InternalOpenAIClient.interpret_code] Error Details: {str(e)}")
                    continue
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant.id)
        except Exception as e:
            print(f"[InternalOpenAIClient.interpret_code] An error occurred while cleaning up the file storage, assistant, and thread.")
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
        return texts, downloaded_files, downloaded_images

    def generate_image(self, prompt: str, image_size: str, quality: str):
        response = {"success": False, "message": "", "image_url": ""}
        image_generation_model = DEFAULT_IMAGE_GENERATION_MODEL

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
            with open(edit_image_uri, "rb") as edit_image_file:
                edit_image_bytes = edit_image_file.read()
            with open(edit_image_mask_uri, "rb") as mask_image_file:
                mask_image_bytes = mask_image_file.read()

            image_modification_response = self.connection.images.edit(
                model=image_modification_model, image=edit_image_bytes, mask=mask_image_bytes,
                prompt=prompt, n=DEFAULT_IMAGE_MODIFICATION_N, size=image_size
            )
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
            with open(image_uri, "rb") as image_file:
                image_bytes = image_file.read()

            image_variation_response = self.connection.images.create_variation(
                model=image_variation_model,
                image=image_bytes,
                n=DEFAULT_IMAGE_VARIATION_N,
                size=image_size
            )
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
                audience = DEFAULT_STATISTICS_ASSISTANT_AUDIENCE,
                tone = DEFAULT_STATISTICS_ASSISTANT_TONE,
                chat_name = DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME)

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
            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            response = choice_message_content
        except Exception as e:
            response = get_statistics_analysis_error_log(error_logs=str(e))
        return response
