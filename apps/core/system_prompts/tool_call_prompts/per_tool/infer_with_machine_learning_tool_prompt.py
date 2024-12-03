#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_predict_ml_models_execution_tool_prompt.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.tool_calls.utils import ToolCallDescriptorNames
from config.settings import MEDIA_URL


def build_tool_prompt__infer_with_machine_learning():
    response_prompt = f"""
            ### **TOOL**: Predict with ML Model Execution Tool

            - The Predict with ML Model Execution Tool is a tool allows you to execute predictions on a machine
            learning model. You can use this to execute operations on a machine learning model to retrieve
            predictions from it. You can use this to describe a code operation to be executed, or an analysis to be
            performed on an ML model, which will be processed by a distinct LLM agent. For example, if you want a
            prediction to be generated based on a data file, the code will be written and ran by a distinct LLM agent
            and you will retrieve the result in terms of text, files, and images. You can ask for the agent to provide
            a summary or analysis based on prediction, and the agent will provide you with the analysis or summary
            in natural language. You are then expected to deliver this in your own words to the user, based on your
            instructions and the needs of the user.

            - The format for dictionary you will output to use Predict with ML Model Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_INFER_WITH_ML}",
                    "parameters": {{
                        "ml_base_connection_id": "...",
                        "model_path": "...",
                        "input_data_paths": ["...", "...", "..."],
                        "query": "..."
                    }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "ml_model_connection_id" must be the ID of the ML model
            connection you need to execute the prediction on. The "model_path" must be the path of the ML model you
            would like to execute the prediction on. The "input_data_paths" must be a list of strings containing the
            paths of the input data you need to execute the prediction on. While choosing the input data paths, you
            can take a look at the names and descriptions of the elements inside the ML model connection to understand
            which input data can be helpful for generating prediction. The "query" must be the query you need to
            execute on the prediction, ALWAYS in NATURAL LANGUAGE. Even if you want to execute a code operation, you
            must write what you want to do in natural language, as writing the code and executing the operations will
            be done by a distinct LLM agent. You can write the query in a way you want to ask a question to a human,
            and the agent will understand and execute accordingly based on the natural language query you provided.

            To use this, you need to provide the following fields 'VERY CAREFULLY':

            - [1] For "ml_model_connection_id", provide ID of the ML model connection you want to execute prediction on

            - [2] For "model_path", provide path of the ML model you want to execute the prediction on.

            - [3] For "file_paths", provide a list of strings containing paths of input data you want to execute the
            prediction on. You can at most provide 10 input paths in list at once. If you think you need to provide
            more than 10, you can provide input data paths in multiple executions of the tool.

            - [4] For "query", provide query you need to execute on the media item, in NATURAL LANGUAGE.

                - *Example Queries:*
                    - "What disease do you think is present in this chest x-ray image?"
                    - "Which handwritten digit do you think is present in this image?"
                    - "Take these 5 images and tell me which ones are classified as dogs and which ones are classified
                        as cats."

                - You ALWAYS need to provide queries in the "query" field, and in natural language.

            ---

            #### **IMPORTANT NOTES:**

            - **NOTE**: The system will provide you the results in next 'assistant' message. This message will
            have the output of the execution, and you will be expected to take this and provide an answer
            to user's question based on the response you received, in your own words. Think of this as an employee
            you are instructing to execute a query on a media item, and you are expected to take the response of this
            employee and provide an answer to the user's question. The response might include text, files, and images
            which you can let user see by sharing in markdown format, or you can provide a link to media item by
            sticking to the following rules:

            #### **ABOUT YOU PROVIDING LINKS:**

            - If you need to provide a direct link to user for reaching files or images, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                - {MEDIA_URL}

            - **NEVER, EVER:** provide a 'relative' path to files or images. Always provide 'absolute' path by
            appending the file path to the base URL.

            ---

        """
    return response_prompt
