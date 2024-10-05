#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps._services.tools.utils import ToolTypeNames
from config.settings import MEDIA_URL


def build_structured_tool_prompt__predict_with_ml_model_execution():
    response_prompt = f"""
            **TOOL**: Predict with ML Model Execution Tool

            - The Predict with ML Model Execution Tool is a tool that allows you to execute predictions on a machine
            learning model. You can use this tool to execute predictions on a machine learning model to retrieve
            predictions from the model. You can use this tool to describe a code operation to be executed, or an
            analysis to be performed on a machine learning model, which will be processed by a distinct GPT agent.
            For example, if you want a prediction to be generated based on a data file, the code will be written and
            ran by a distinct GPT assistant and you will simply retrieve the result in terms of text, files and images.
            You can also ask for the assistant to provide a summary or analysis based on the prediction, and the
            assistant will provide you with the analysis or summary in natural language. You are then expected to
            deliver this response in your own words to the user, based on your instructions and the needs of the user.

            - The standardized format for the dictionary that you will output to use the Predict with ML Model Execution
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.PREDICTION_WITH_ML_MODEL}",
                    "parameters": {{
                        "ml_base_connection_id": "...",
                        "model_path": "...",
                        "input_data_paths": ["...", "...", "..."],
                        "query": "..."
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "ml_model_connection_id" field should be the ID of the machine learning model
            connection that you would like to execute the prediction on. The "model_path" field should be the path of
            the machine learning model that you would like to execute the prediction on. The "input_data_paths" field
            should be a list of strings that contain the paths of the input data that you would like to execute the
            prediction on. While choosing the input data paths, you can take a look at the names and descriptions of
            the elements inside the machine learning model connection to understand which input data can be helpful
            for generating the prediction. The "query" field should be the query that you would like to execute on the
            prediction, in NATURAL LANGUAGE ALWAYS. Even if you would like to execute a code operation, you should write
            what you want to do in natural language, because writing the code and executing the operations will be done
            by a distinct GPT assistant. You can write the query in a way that you would like to ask a question to a
            human, and the assistant will understand and execute the query based on the natural language query that you
            provide.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "ml_model_connection_id", provide the ID of the machine learning model connection that you would
            like to execute the prediction on.

            2. For "model_path", provide the path of the machine learning model that you would like to execute the
            prediction on.

            3. For "file_paths", provide a list of strings that contain the paths of the input data that you would
            like to execute the prediction on. You can at most provide 10 input data paths in the list at once. If you
            think you need to provide more than 10 input data paths, you can provide the input data paths in multiple
            executions of the tool.

            4. For "query", provide the query that you would like to execute on the media item, in NATURAL LANGUAGE,
            ALWAYS.
                - *Example Queries:*
                    - "What disease do you think is present in this chest x-ray image?"
                    - "Which handwritten digit do you think is present in this image?"
                    - "Take these 5 images and tell me which ones are classified as dogs and which ones are classified
                        as cats."
                - You always need to provide the queries in the "query" field, and in natural language.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words. Think of this tool
            as an employee of yours that you are instructing to execute a query on a media item, and you are expected
            to take the response of this employee and provide an answer to the user's question based on the response
            that you receive from this employee. The response might include text, files, and images which you can
            let the user see by sharing in markdown format, or you can provide a link to the media item by sticking to
            the following rules:

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the file or images, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to the file or image. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """
    return response_prompt
