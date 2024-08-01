

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


HELPER_ASSISTANT_PROMPTS = {
    "code_interpreter": {
        "name": "Code Interpreter Assistant",
        "description": """
            *NEVER ASK QUESTIONS, JUST DO THE JOB.*
            '''
            You are a Code Interpreter Assistant. You are responsible for writing + executing code and provide
            the best answer based on the code you executed. You are capable of writing and executing
            code to help the user.
            '''

            Your answer should be clear, concise, and to the point. Use your code interpreter to provide
            accurate and detailed information.

        """,
    },
    #################################################################################################################
    "file_interpreter": {
        "name": "File Interpretation & Analysis Assistant",
        "description": """
            *NEVER ASK QUESTIONS, JUST DO THE JOB.*
            '''
            You are a File Interpretation & Analysis Assistant. You are responsible for reading, interpreting the
            files and data, and provide users with the best answer based on the information you have extracted.
            '''

            Your answer should be clear, concise, and to the point. Use your code interpreter to provide
            accurate and detailed information.

        """,
        "model": "gpt-4o",
    },
    #################################################################################################################
    "image_interpreter": {
        "name": "Image Interpretation & Analysis Assistant",
        "description": """
            *NEVER ASK QUESTIONS, JUST DO THE JOB.*
            '''
            You are an Image Interpretation & Analysis Assistant. You are responsible for interpreting the images
            and provide users with the best answer based on the information you have extracted.
            '''

            Your answer should be clear, concise, and to the point. Use your code interpreter to provide
            accurate and detailed information.

        """,
        "model": "gpt-4o",
    },
    #################################################################################################################
    "ml_model_predictor": {
        "name": "Machine Learning Model Predictor Assistant",
        "description": """
            *NEVER ASK QUESTIONS, JUST DO THE JOB.*
            '''
            You are a Machine Learning Model Predictor Assistant. You take in a pre-trained torch model and input
            data, prepare the data for the model, feed it to the model, and provide the prediction results.
            '''

            Your answer should be clear, concise, and to the point. Use your code interpreter to provide
            accurate and detailed information.

        """,
        "model": "gpt-4o",
    },
}


GENERATE_FILE_DESCRIPTION_QUERY = f"""
    Please interpret the file or image I sent you, and provide a clear and concise description about the contents
    within the image. Do not write an overly long description, and keep it to the point. It would be the best
    if your description is less than 1000 characters in total. Make sure your interpretations are accurate and
    does not contain subjective opinions; but instead focus on the facts and information that can be extracted
    from the image or file itself.

    **NOTE:** You must deliver the description in plain text format, without markdown elements or any other
    special formatting, nor lists, multiple paragraphs, or bullet points. Just a single paragraph of plain text
    is what I need.
"""


ONE_SHOT_AFFIRMATION_PROMPT = f"""

    **Affirmation Prompt**
    - DO NOT ASK QUESTIONS TO ME. YOU ARE A ZERO-SHOT MODEL, PEOPLE WON'T CHAT WITH YOU, JUST PROVIDE YOUR BEST ANSWER.
    - DO NOT ASK QUESTIONS TO ME. YOU ARE A ZERO-SHOT MODEL, PEOPLE WON'T CHAT WITH YOU, JUST PROVIDE YOUR BEST ANSWER.
    - DO NOT ASK QUESTIONS TO ME. YOU ARE A ZERO-SHOT MODEL, PEOPLE WON'T CHAT WITH YOU, JUST PROVIDE YOUR BEST ANSWER.
    - DO NOT ASK QUESTIONS TO ME. YOU ARE A ZERO-SHOT MODEL, PEOPLE WON'T CHAT WITH YOU, JUST PROVIDE YOUR BEST ANSWER.
    - DO NOT ASK QUESTIONS TO ME. YOU ARE A ZERO-SHOT MODEL, PEOPLE WON'T CHAT WITH YOU, JUST PROVIDE YOUR BEST ANSWER.
"""

ML_AFFIRMATION_PROMPT = f"""

    **Machine Learning Affirmation Prompt**
    - NEVER USE KERAS AND TENSORFLOW. ALWAYS USE PYTORCH. ALWAYS USE THE MODEL THAT IS SHARED WITH YOU, DO NOT DEVELOP MODELS YOURSELF.
    - NEVER USE KERAS AND TENSORFLOW. ALWAYS USE PYTORCH. ALWAYS USE THE MODEL THAT IS SHARED WITH YOU, DO NOT DEVELOP MODELS YOURSELF.
    - NEVER USE KERAS AND TENSORFLOW. ALWAYS USE PYTORCH. ALWAYS USE THE MODEL THAT IS SHARED WITH YOU, DO NOT DEVELOP MODELS YOURSELF.
    - NEVER USE KERAS AND TENSORFLOW. ALWAYS USE PYTORCH. ALWAYS USE THE MODEL THAT IS SHARED WITH YOU, DO NOT DEVELOP MODELS YOURSELF.
    - NEVER USE KERAS AND TENSORFLOW. ALWAYS USE PYTORCH. ALWAYS USE THE MODEL THAT IS SHARED WITH YOU, DO NOT DEVELOP MODELS YOURSELF.
"""

INSUFFICIENT_BALANCE_PROMPT = f"""
    **SYSTEM MESSAGE:**
    - It seems like you don't have enough balance to continue this conversation. Please contact your organization's
    administrator to top up your balance, or if you have the necessary permissions, you can top up your balance
    yourself. If you encounter any problems during the balance top-up process, please connect the support team to
    get guidance.
"""


EMPTY_FILE_PATH_LOG = f"""
    **SYSTEM MESSAGE:**
    - The file path is empty.
"""


FILE_INTERPRETER_PREPARATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the assistant for the file interpretation.
"""


FILE_INTERPRETER_THREAD_CREATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the thread for the file interpretation.
"""

FILE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while retrieving the response from the file interpreter assistant.
"""


FILE_STORAGE_CLEANUP_ERROR_LOG = f"""
    **SYSTEM MESSAGE**:
     - An error occurred while cleaning up the file storage, assistant, and thread.
"""

IMAGE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while retrieving the response from the image interpreter assistant.
"""

IMAGE_INTERPRETER_RESPONSE_PROCESSING_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while processing the response from the image interpreter assistant.
"""

ML_MODEL_NOT_FOUND_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - The model could not be found.
"""

ML_MODEL_LOADING_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while loading the model.
"""

ML_MODEL_OPENAI_UPLOAD_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
     - An error occurred while uploading the model to the OpenAI server.
"""

ML_MODEL_ASSISTANT_PREPARATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the assistant for the ML model prediction.
"""

ML_MODEL_THREAD_CREATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the thread for the ML model prediction.
"""

ML_MODEL_RESPONSE_RETRIEVAL_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while retrieving the response from the ML model prediction assistant.
"""

ML_MODEL_CLEANUP_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while cleaning up the file storage, assistant, and thread.
"""


CODE_INTERPRETER_ASSISTANT_PREPARATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the assistant for the code interpretation.
"""

CODE_INTERPRETER_THREAD_CREATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the thread for the code interpretation.
"""

CODE_INTERPRETER_RESPONSE_RETRIEVAL_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while retrieving the response from the code interpreter assistant.
"""

CODE_INTERPRETER_CLEANUP_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while cleaning up the file storage, assistant, and thread.
"""


def get_maximum_tool_chains_reached_log(final_response:str):
    log = f"""
        {final_response}

        ---

        System Message:

        The maximum number of tool chains has been reached. No further tool chains can be executed.
        If you believe you need to be able to chain more tools, please increase the limit in the assistant
        settings.

        The response retrieval cycle will be stopped now.

        ---

    """
    return log


def get_maximum_tool_attempts_reached_log(final_response: str):
    log = f"""
        {final_response}

        ---

        System Message:

        The maximum number of attempts for the tool has been reached. No further attempts can be made
        for retrieval via this tool in this request. If you believe you need to be able to make more
        attempts for using the same tool, please increase the limit in the assistant settings.

        The response retrieval cycle will be stopped now.

    """
    return log


def get_technical_error_log(error_logs: str):
    return f"""
        Technical Details about the Error:

            If the issue persists, please contact the system administrator and deliver the error message below to
            provide a solution to the problem as soon as possible.

            '''
            {str(error_logs)}
            '''
"""


def get_json_decode_error_log(error_logs: str):
    return f"""
        **SYSTEM MESSAGE:**

        - An error occurred while decoding the JSON response provided by the AI assistant. This might be
        related to the incorrect formatting of the response. Please make sure that the response is in the
        correct JSON format.

        Error Details:
        '''
        {str(error_logs)}
        '''
    """


def embed_tool_call_in_prompt(json_parts_of_response: str):
    prompt = f"""
    **Assistant Tool Call:**

    ```

    {json_parts_of_response}

    ```
    """
    return prompt


def get_number_of_files_too_high_log(max):
    return f"""
        **SYSTEM MESSAGE:**
        - The number of files to be interpreted is too high. Please provide a smaller number of files.
        The maximum number supported by the system is {max}.
    """


def get_number_of_ml_predictions_too_high_log(max):
    return f"""
        **SYSTEM MESSAGE:**
        - The number of input data to be predicted is too high. Please provide a smaller number of input data.
        The maximum number supported by the system is {max}.
    """


def get_number_of_codes_too_high_log(max):
    return f"""
        **SYSTEM MESSAGE:**
        - The number of codes to be executed is too high. Please provide a smaller number of codes.
        The maximum number supported by the system is {max}.
    """


def get_file_interpreter_status_log(status):
    return f"""
        **SYSTEM MESSAGE:**
        - The file interpretation process has {status} on the OpenAI server.
    """


def get_ml_prediction_status_log(status):
    return f"""
        **SYSTEM MESSAGE:**
        - The ML model prediction process has {status} on the OpenAI server.
    """


def get_code_interpreter_status_log(status):
    return f"""
        **SYSTEM MESSAGE:**
        - The code interpretation process has {status} on the OpenAI server.
    """


def get_image_generation_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while generating the image.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_image_modification_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while modifying the image.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_image_variation_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while creating variation of the image.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_statistics_analysis_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while analyzing the statistics.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """
