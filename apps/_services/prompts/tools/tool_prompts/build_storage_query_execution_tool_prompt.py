#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: build_storage_query_execution_tool_prompt.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:12:15
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.tools.utils import ToolTypeNames
from config.settings import MEDIA_URL


def build_structured_tool_prompt__media_storage_query_execution():
    response_prompt = f"""
            **TOOL**: Media Storage Query Execution Tool

            - The Media Storage Query Execution Tool is a tool that allows you to execute queries on a media storage
            connection. You can use this tool to execute queries on a media storage connection to retrieve information
            from the media storage connection. You can use this tool to describe a code operation to be executed, or
            an analysis to be performed on a media item, which will be processed by a distinct GPT agent. For example,
            if you want a chart to be generated based on a data file, the code will be written and ran by a distinct
            GPT assistant and you will simply retrieve the result in terms of text, files and images. Another example
            is that you can ask for the assistant to provide a summary or analysis based on a certain image or media,
            and the assistant will provide you with the analysis or summary in natural language. You are then
            expected to deliver this response in your own words to the user, based on your instructions and the
            needs of the user.

            - The standardized format for the dictionary that you will output to use the Media Storage Query Execution
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.MEDIA_STORAGE_QUERY_EXECUTION}",
                    "parameters": {{
                        "media_storage_connection_id": "...",
                        "type": "file_interpretation" or "image_interpretation",
                        "file_paths": ["...", "...", "..."],
                        "query": "..."
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "media_storage_connection_id" field should be the ID of the media storage connection
            that you would like to execute the query on. The "type" field should be the type of interpretation that you
            would like to perform on the media item, which must be one of the following: "file_interpretation" or
            "image_interpretation". The "file_paths" field should be a list of strings that contain the paths of the
            media items that you would like to execute the query on. While choosing the file paths, you can take a
            look at the names and descriptions of the elements inside the media storage connection to understand which
            media items can be helpful for answering the user's question or for helping him/her. The "query" field
            should be the query that you would like to execute on the media item, in NATURAL LANGUAGE, ALWAYS. Even
            if you would like to execute a code operation, you should write what you want to do in natural language,
            because writing the code and executing the operations will be done by a distinct GPT assistant. You can
            write the query in a way that you would like to ask a question to a human, and the assistant will
            understand and execute the query based on the natural language query that you provide.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "media_storage_connection_id", provide the ID of the media storage connection that you would like
            to execute the query on.

            2. For "type", provide the type of interpretation that you would like to perform on the media item, which
            must be one of the following: "file_interpretation" or "image_interpretation".

            3. For "file_paths", provide a list of strings that contain the paths of the media items that you would
            like to execute the query on. You can at most provide 20 file paths in the list at once. If you think you
            need to provide more than 20 file paths, you can run the tool again to provide more file paths.

            4. For "query", provide the query that you would like to execute on the media item, in NATURAL LANGUAGE,
            ALWAYS.
                - *Example Queries:*
                    - "Please provide a summary of the image."
                    - "Please show the descriptive statistics of the file."
                    - "Please provide a chart based on the data in the file."
                    - "Please take in these two images and provide a comparison between them."
                - You always need to provide the queries in the "query" field, and in natural language.

            ---

            **IMPORTANT NOTES:**

            - *IMAGE PREFIXES*:
                - If the image URI you have includes a prefix 'free_form__user_sketch__', this means that the image
                is a user sketch. This information is shared with you so that you can understand that the user drew
                this picture while interacting with you, within the chat interface. You can use this information to
                provide a more accurate response to the user's question.

            - "NEVER, EVER" try to operate on "files" and "images" at the same time. Instead of this approach, first
            operate on the "files" and then operate on the "images" in a separate operation. This is because the
            system will not be able to understand which operation you would like to perform if you provide both
            "files" and "images" at the same time and fail to execute the query.

            - For file interpretations, you will receive three fields in the output; the textual outputs for
            representing the response of the query, the file URIs for representing the URIs of the files that are
            generated as a result of the query, and the image URIs for representing the URIs of the images that are
            generated as a result of the query. The image and file URIs can be empty depending on the query that you
            provide.

            - For image interpretations, you will receive a single field which will represent the textual response,
            representing the response of the query by the assistant.

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words. Think of this tool
            as an employee of yours that you are instructing to execute a query on a media item, and you are expected
            to take the response of this employee and provide an answer to the user's question based on the response
            that you receive from this employee.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the file or images, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to the file or image. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """

    return response_prompt
