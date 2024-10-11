#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: status_log_prompts.py
#  Last Modified: 2024-10-08 23:48:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 23:48:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


def get_number_of_files_too_high_log(max):
    return f"""
        **SYSTEM MESSAGE:**
        - The number of files to be interpreted is too high. Provide a smaller number of files. The maximum number
        supported by the system is {max}.
    """


def get_number_of_ml_predictions_too_high_log(max):
    return f"""
        **SYSTEM MESSAGE:**
        - The number of input data to be predicted is too high. Please provide a smaller number of input data. The
        maximum number supported by the system is {max}.
    """


def get_number_of_codes_too_high_log(max):
    return f"""
        **SYSTEM MESSAGE:**
        - The number of codes to be executed is too high. Please provide a smaller number of codes. The maximum number
        supported by the system is {max}.
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
        - The code analysis process has {status} on the OpenAI server.
    """
