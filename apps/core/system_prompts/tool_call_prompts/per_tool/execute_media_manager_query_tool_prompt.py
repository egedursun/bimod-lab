#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_storage_query_execution_tool_prompt.py
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

from apps.core.tool_calls.utils import (
    ToolCallDescriptorNames
)

from config.settings import MEDIA_URL


def build_tool_prompt__media_manager_query():
    response_prompt = f"""

            ### **TOOL**: Media Storage Query Execution Tool

            - The Media Storage Query Execution Tool is a tool allows you to execute queries on a media storage
            connection. You can use this to execute queries on a media storage to retrieve info from media storage
            connection. You can use this to describe a code operation to be executed, or an analysis to be performed
            on a media item, which will be processed by a distinct LLM agent. For example, if you want a chart to be
            generated based on a data file, the code will be written and ran by a distinct assistant and you will
            retrieve the result in terms of text, files, and images. Another example is you can ask for the agent to
            provide a summary or analysis based on a certain image/media, and assistant will provide you with analysis
            or summary in natural language. You are then expected to deliver response in your own words to user,
            based on your instructions and needs of the user.

            - The format for dictionary you will output to use Media Storage Query Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_MEDIA_MANAGER_QUERY}",
                    "parameters": {{
                        "media_storage_connection_id": "...",
                        "type": "file_interpretation" or "image_interpretation",
                        "file_paths": ["...", "...", "..."],
                        "query": "..."
                    }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "media_storage_connection_id" must be ID of media storage connection
            you need to execute query on. The "type" must be type of interpretation you need to perform on the media
            item, which must be one of the following: "file_interpretation" or "image_interpretation". The "file_paths"
            must be a list of strings containing paths of media items you need to execute the query. While choosing
            file paths, you can take a look at the names and descriptions of elements inside media storage connection
            to understand which media items can be helpful for answering user's question or for helping him/her.
            The "query" must be the query you would like to execute on media item, in NATURAL LANGUAGE, ALWAYS. Even
            if you want to execute a code operation, you must write what you want to do in natural language,
            as writing the code and executing operations will be done by a distinct LLM assistant. You can write the
            query in a way you need to ask a question to a human, and the assistant will understand and execute query
            based on natural language query you provide.

            To use this, you need to provide the following fields 'VERY CAREFULLY':

            - [1] For "media_storage_connection_id", provide ID of media storage connection you would like to execute
            the query on.

            - [2] For "type", provide type of interpretation you need to perform on media item, which must be one of
            the following: "file_interpretation" or "image_interpretation".

            - [3] For "file_paths", provide a list of strings containing the paths of the media items you need to
            execute the query. You can at most provide 20 file paths in the list at once. If you think you need to
            provide more than 20, you can run the tool again later to provide more paths.

            - [4] For "query", provide query you need to execute on media item, in NATURAL LANGUAGE, ALWAYS.

                - *Example Queries:*
                    - "Please provide a summary of the image."
                    - "Please show the descriptive statistics of the file."
                    - "Please provide a chart based on the data in the file."
                    - "Please take in these two images and provide a comparison between them."

                - You always need to provide the queries in the "query" field, and in natural language.

            ---

            #### **IMPORTANT NOTES:**

            - *IMAGE PREFIXES*:

                - If the image URI you have includes a prefix 'free_form__user_sketch__', this means the image
                is a user sketch. This info is shared with you so you can understand the user drew this picture
                while interacting within the chat interface. You can use this info to provide a more accurate
                response to user's question.

            - "NEVER, EVER" try to operate on "files" and "images" at the same time. Instead of this, first
            operate on "files" and then operate on "images" in "separate operations". This is because the
            system will not be able to understand which operation you need to perform if you provide both
            "files" and "images" the same time and FAIL to execute your query.

            - For file interpretations, you will receive 3 fields in output; the textual outputs for
            representing the response of query, the file URIs for representing URIs of files that are generated as a
            result of query, and image URIs for representing URIs of images that are generated as a result of query.
            The image and file URIs can be empty depending on query you provide.

            - For image interpretations, you will receive a single field which represents the textual response,
            representing response of the query by the agent.

            **NOTE**: The system will provide you the results in next 'assistant' message. This message will have the
            output of the execution, and you will be expected to take this response and provide an answer
            to user's question based on what you receive, in your own words. Think of this tool as an employee
            you are instructing to execute a query on a media item, and you are expected to take the response of this
            employee and provide an answer to user's question.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a direct link to user for reaching files or images, here is the base
                    URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to the file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' path to files or images. Always provide 'absolute' path by
                appending file path to the base URL.

            ---

        """

    return response_prompt
