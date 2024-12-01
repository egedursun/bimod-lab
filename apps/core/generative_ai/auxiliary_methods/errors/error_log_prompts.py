#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: error_log_prompts.py
#  Last Modified: 2024-10-08 23:47:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 23:47:20
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

ANALYST_PREPARATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the agent for the file interpretation.
"""

ANALYST_THREAD_CREATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the thread for the file interpretation.
"""

ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while retrieving the response from the file interpreter assistant.
"""

MEDIA_MANAGER_CLEANUP_ERROR_LOG = f"""
    **SYSTEM MESSAGE**:
     - An error occurred while cleaning up the file storage, assistant, and thread.
"""

IMAGE_ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while retrieving the response from the image interpreter assistant.
"""

IMAGE_ANALYST_RESPONSE_PROCESSING_ERROR_LOG = f"""
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

ML_MODEL_AGENT_PREPARATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the agent for the ML model prediction.
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

CODE_ANALYST_AGENT_PREPARATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the agent for the code interpretation.
"""

CODE_ANALYST_THREAD_CREATION_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while preparing the thread for the code interpretation.
"""

CODE_ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while retrieving the response from the code interpreter assistant.
"""

CODE_ANALYST_CLEANUP_ERROR_LOG = f"""
    **SYSTEM MESSAGE:**
    - An error occurred while cleaning up the file storage, assistant, and thread.
"""


def get_technical_error_log(error_logs: str):
    return f"""
        Technical Details about the Error:

            If the issue persists, please contact the platform administrator and deliver the error message below to
            provide a solution to the problem as soon as possible.

            '''
            {str(error_logs)}
            '''
"""


def get_json_decode_error_log(error_logs: str):
    return f"""
        **SYSTEM MESSAGE:**

        - An error occurred while decoding the JSON. This can be related to the incorrect formatting.
        Please make sure that the response is in the correct JSON format.

        Error Details:
        '''
        {str(error_logs)}
        '''
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
    - An error occurred while editing the image.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_image_variation_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while dreaming variation of the image.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_statistics_analysis_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while analyzing the tenant statistics.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_audio_reading_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while reading the audio file.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_audio_transcription_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while transcribing the audio.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_audio_generation_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while generating the audio.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_audio_upload_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while uploading the audio.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """


def get_no_reasoning_capability_error_log():
    return f"""
    **SYSTEM MESSAGE:**
    - The agent does not have the reasoning capability. If you would like to use the reasoning capability,
    please enable it in the agent settings.
    """


def get_default_reasoning_error_log(error_logs: str):
    return f"""
    **SYSTEM MESSAGE:**
    - An error occurred while processing the reasoning operation request.

    Error Details:
    '''
    {str(error_logs)}
    '''
    """
