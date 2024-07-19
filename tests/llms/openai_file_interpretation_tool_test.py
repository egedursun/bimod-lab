import time

from openai import OpenAI
from openai._legacy_response import HttpxBinaryResponseContent
from openai.types.beta.threads import TextContentBlock, ImageFileContentBlock

from apps._services.llms.helpers.helper_prompts import HELPER_ASSISTANT_PROMPTS, AFFIRMATION_PROMPT


#######################################################################################################################
# ENUMERATIONS
#######################################################################################################################

class ChatRoles:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AssistantRunStatuses:
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REQUIRES_ACTION = "requires_action"
    EXPIRED = "expired"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    FAILED = "failed"
    INCOMPLETE = "incomplete"

#######################################################################################################################
#######################################################################################################################


def ask_about_file(client, full_file_paths: list, query_string: str):

    # start timer
    timer_start = time.time()

    if len(full_file_paths) > 20:
        return ("System Message: The number of files to be interpreted is too high. Please provide a smaller "
                "number of files. The maximum number supported by the system is 20.")

    timer_validation = time.time()
    print(f"Validation Time: [{timer_validation - timer_start}] seconds.")

    file_contents = []
    for path in full_file_paths:
        if not path:
            return "System Message: The file path is empty."

        try:
            # Read binary file contents
            with open(path, "rb") as file:
                file_contents.append(file.read())
        except FileNotFoundError:
            print(f"System Message: The file at the path '{path}' could not be found, skipping file...")
            continue
        except Exception as e:
            print(f"System Message: An error occurred while reading the file at the path '{path}', "
                  f"skipping file...")
            print(f"Error Details: {str(e)}")
            continue

    if not file_contents:
        return "System Message: No file contents could be read from the provided file paths."

    timer_file_reading = time.time()
    print(f"File Reading Time: [{timer_file_reading - timer_validation}] seconds.")

    # Upload the file to OpenAI server
    file_objects = []
    for content in file_contents:
        file = client.files.create(
            purpose="assistants",
            file=content
        )
        file_objects.append(file)

    timer_file_upload = time.time()
    print(f"File Upload Time: [{timer_file_upload - timer_file_reading}] seconds.")

    # Prepare the assistant for the file interpretation
    assistant = client.beta.assistants.create(
        name=HELPER_ASSISTANT_PROMPTS["file_interpreter"]["name"],
        description=HELPER_ASSISTANT_PROMPTS["file_interpreter"]["description"],
        model="gpt-4o",
        tools=[{"type": "code_interpreter"}],
        tool_resources={
            "code_interpreter": {
                "file_ids": [x.id for x in file_objects]
            }
        },
        temperature=0.25
    )

    timer_assistant_creation = time.time()
    print(f"Assistant Creation Time: [{timer_assistant_creation - timer_file_upload}] seconds.")

    # Prepare the thread
    thread = client.beta.threads.create(
        messages=[
            {
                "role": ChatRoles.USER,
                "content": (query_string + AFFIRMATION_PROMPT),
            }
        ]
    )

    timer_thread_creation = time.time()
    print(f"Thread Creation Time: [{timer_thread_creation - timer_assistant_creation}] seconds.")

    # Retrieve the response from the assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    timer_run_creation = time.time()
    print(f"Query Run Time: [{timer_run_creation - timer_thread_creation}] seconds.")

    # Format and get the messages
    texts, image_download_ids, file_download_ids = [], [], []
    if run.status == AssistantRunStatuses.COMPLETED:
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
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
        else:
            messages = f"System Message: Terminal {run.status.upper()} status on the OpenAI server."
    # END IF

    timer_message_classification = time.time()
    print(f"Message Classification Time: [{timer_message_classification - timer_run_creation}] seconds.")

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

    timer_retrieval_files = time.time()
    print(f"File Retrieval Time: [{timer_retrieval_files - timer_message_classification}] seconds.")

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

    timer_retrieval_images = time.time()
    print(f"Image Retrieval Time: [{timer_retrieval_images - timer_retrieval_files}] seconds.")

    # Clean the file storage
    for file in file_objects:
        try:
            client.files.delete(file.id)
        except Exception as e:
            print(f"System Message: An error occurred while deleting the file with ID '{file.id}'.")
            print(f"Error Details: {str(e)}")
            continue

    # Delete the thread and the assistant
    client.beta.threads.delete(thread.id)
    client.beta.assistants.delete(assistant.id)

    timer_cleaning = time.time()
    print(f"Cleaning Time: [{timer_cleaning - timer_retrieval_images}] seconds.")

    # stop timer
    timer_end = time.time()
    print(f"Time taken: [{timer_end - timer_start}] seconds.")

    print(messages)
    print(texts)
    print(downloaded_files)
    print(downloaded_images)


OPENAI_API_KEY = "sk-proj-AfSj7ohaxbXDQf2WLLSUT3BlbkFJGZifjSfVePMOJtBeRz5V"
file_path_1 = './customers-100.csv'  # put the CSV data file here
file_path_2 = './jeopardy.xlsx'  # put an Excel file here for testing

c = OpenAI(api_key=OPENAI_API_KEY)

ask_about_file(c,
               [file_path_1],
               "Create an empty chart.")
