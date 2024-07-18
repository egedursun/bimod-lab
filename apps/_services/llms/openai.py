import json
import re
import base64 as b64

from openai import OpenAI
from openai.types.beta.threads import TextContentBlock, ImageFileContentBlock

from apps._services.llms.helpers.helper_prompts import HELPER_ASSISTANT_PROMPTS, AssistantRunStatuses
from apps._services.prompts.history_builder import HistoryBuilder
from apps._services.prompts.prompt_builder import PromptBuilder
from apps._services.tools.tool_executor import ToolExecutor
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.multimodal_chat.utils import calculate_billable_cost_from_raw
from config.settings import BASE_URL


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

CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION = 20


def retry_mechanism(client, latest_message):
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
                 assistant,
                 multimodal_chat
                 ):
        self.connection = OpenAI(
            api_key=assistant.llm_model.api_key,
        )
        self.assistant = assistant
        self.chat = multimodal_chat

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
                tool_response, tool_name, file_uris, image_uris = tool_executor.use_tool()
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
                message_text_content=tool_response,
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
            return self.respond(latest_message=tool_message, prev_tool_name=prev_tool_name, with_media=with_media,
                                file_uris=file_uris, image_uris=image_uris)

        # reset the active chain size
        ACTIVE_CHAIN_SIZE = 0

        # for export assistants API
        if with_media:
            file_uris = [f"{BASE_URL}/{x}" for x in file_uris]
            image_uris = [f"{BASE_URL}/{x}" for x in image_uris]
            return final_response, file_uris, image_uris
        return final_response

    def ask_about_file(self, full_file_paths: list, query_string: str, interpretation_temperature: float,
                       interpretation_maximum_tokens: int):
        client = self.connection
        if len(full_file_paths) > 20:
            return ("System Message: The number of files to be interpreted is too high. Please provide a smaller "
                    "number of files. The maximum number supported by the system is 20."), [], []

        file_contents = []
        for path in full_file_paths:
            if not path: return "System Message: The file path is empty.", [], []
            try: # Read binary file contents
                with open(path, "rb") as file: file_contents.append(file.read())
            except FileNotFoundError:
                print(f"System Message: The file at the path '{path}' could not be found, skipping file...")
                continue
            except Exception as e:
                print(f"System Message: An error occurred while reading the file at the path '{path}', "
                      f"skipping file...")
                print(f"Error Details: {str(e)}")
                continue

        if not file_contents: return "System Message: No file contents could be read from the provided file paths.", [], []

        # Upload the file to OpenAI server
        file_objects = []
        for content in file_contents:
            try:
                file = client.files.create(purpose="assistants", file=content)
                file_objects.append(file)
            except Exception as e:
                print(f"System Message: An error occurred while uploading the file to the OpenAI server.")
                print(f"Error Details: {str(e)}")
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
            print(f"System Message: An error occurred while preparing the assistant for the file interpretation.")
            print(f"Error Details: {str(e)}")
            return "System Message: An error occurred while preparing the assistant for the file interpretation.", [], []

        # Prepare the thread
        try:
            thread = client.beta.threads.create(messages=[{"role": ChatRoles.USER, "content": query_string,}])
        except Exception as e:
            print(f"System Message: An error occurred while preparing the thread for the file interpretation.")
            print(f"Error Details: {str(e)}")
            return "System Message: An error occurred while preparing the thread for the file interpretation.", [], []

        # Retrieve the response from the assistant
        try:
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
        except Exception as e:
            print(f"System Message: An error occurred while retrieving the response from the file interpreter assistant.")
            print(f"Error Details: {str(e)}")
            return "System Message: An error occurred while retrieving the response from the file interpreter assistant.", [], []

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
                                    file_download_ids.append(file_id)
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
                messages = "System Message: The file interpretation process has failed on the OpenAI server."
            elif run.status == AssistantRunStatuses.INCOMPLETE:
                messages = "System Message: The file interpretation process is incomplete on the OpenAI server."
            elif run.status == AssistantRunStatuses.EXPIRED:
                messages = "System Message: The file interpretation process has expired on the OpenAI server."
            elif run.status == AssistantRunStatuses.CANCELLED:
                messages = "System Message: The file interpretation process has been cancelled on the OpenAI server."
            else: messages = f"System Message: Terminal {run.status.upper()} status on the OpenAI server."
        # END IF

        # Download the generated images and files (if any)
        downloaded_files = []
        for file_id in file_download_ids:
            try:
                binary_content = client.files.content(file_id).read()
                downloaded_files.append(binary_content)
            except Exception as e:
                print(f"System Message: An error occurred while downloading the file with ID '{file_id}'.")
                print(f"Error Details: {str(e)}")
                continue
        # END FOR

        downloaded_images = []
        for image_id in image_download_ids:
            try:
                binary_content = client.files.content(image_id).read()
                downloaded_images.append(binary_content)
            except Exception as e:
                print(f"System Message: An error occurred while downloading the image with ID '{image_id}'.")
                print(f"Error Details: {str(e)}")
                continue
        # END FOR

        # Clean the file storage, assistant, and thread
        try:
            for file in file_objects:
                try: client.files.delete(file.id)
                except Exception as e:
                    print(f"System Message: An error occurred while deleting the file with ID '{file.id}'.")
                    print(f"Error Details: {str(e)}")
                    continue
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant.id)
        except Exception as e:
            print(f"System Message: An error occurred while cleaning up the file storage, assistant, and thread.")
            print(f"Error Details: {str(e)}")
            return "System Message: An error occurred while cleaning up the file storage, assistant, and thread.", [], []

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
        if len(full_image_paths) > 20:
            return ("System Message: The number of images to be interpreted is too high. Please provide a smaller "
                    "number of images. The maximum number supported by the system is 20.")
        image_contents = []
        for path in full_image_paths:
            if not path:
                return "System Message: The image path is empty."

            try:
                # Read binary image contents
                with open(path, "rb") as file: image_contents.append({"binary": file.read(), "extension": path.split(".")[-1]})
            except FileNotFoundError:
                print(f"System Message: The image at the path '{path}' could not be found, skipping image...")
                continue
            except Exception as e:
                print(f"System Message: An error occurred while reading the image at the path '{path}', skipping image...")
                print(f"Error Details: {str(e)}")
                continue

        # Convert binaries to base64
        image_objects = []
        for image_content in image_contents:
            binary = image_content["binary"]
            extension = image_content["extension"]
            # convert to base64
            image_base64 = b64.b64encode(binary).decode("utf-8")
            image_objects.append({"base64": image_base64, "extension": extension})

        # Prepare the thread
        messages = [
            {"role": ChatRoles.SYSTEM,
             "content": [{"type": "text", "text": HELPER_ASSISTANT_PROMPTS["image_interpreter"]["description"]}]},
            {"role": ChatRoles.USER, "content": [{"type": "text", "text": query_string}]}
        ]
        for image_object in image_objects:
            formatted_uri = f"data:image/{image_object['extension']};base64,{image_object['base64']}"
            messages[-1]["content"].append({"type": "image_url", "image_url": {"url": formatted_uri}})
        # END FOR

        # Retrieve the response from the assistant
        try:
            response = client.chat.completions.create(
                model=HELPER_ASSISTANT_PROMPTS["image_interpreter"]["model"],
                messages=messages,
                temperature=interpretation_temperature,
                max_tokens=interpretation_maximum_tokens
            )
        except Exception as e:
            print(f"System Message: An error occurred while retrieving the response from the image interpreter "
                  f"assistant.")
            print(f"Error Details: {str(e)}")
            return ("System Message: An error occurred while retrieving the response from the image interpreter "
                    "assistant.")

        try:
            choices = response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content
        except Exception as e:
            print(f"System Message: An error occurred while processing the response from the image interpreter "
                  f"assistant.")
            print(f"Error Details: {str(e)}")
            return ("System Message: An error occurred while processing the response from the image interpreter "
                    "assistant.")

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
