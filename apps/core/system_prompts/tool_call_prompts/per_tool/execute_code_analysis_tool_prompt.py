#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_code_interpreter_tool_prompt.py
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


def build_tool_prompt__analyze_code():
    response_prompt = f"""
            ### **TOOL**: Code Interpreter Tool

            - The Code Interpreter Tool is a tool allows you to write and execute code operations in an integrated
            Python environment. You can use this to write code operations you want to execute, and the tool assistant
            will execute them and provide you the results. You can also use this to write code operations you want
            to execute on a "specific file". Unlike Media Storage Query Execution Tool, Code Interpreter Tool is a
            dedicated tool for writing & executing code operations for various use cases such as arithmetics, unit
            conversions, sensitive mathematical calculations, and more.

            - The format for dictionary you will output to use Code Interpreter Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_ANALYZE_CODE}",
                    "parameters": {{
                        "file_paths": ["...", "...", "..."],
                        "query": "..."
                    }}
                }}
            '''

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "file_paths" field must be a list of strings containing the paths of data files
            you need to execute the code operation on. You don't have to provide a file path if you don't want
            to execute code operation on a data file. For example, this wouldn't be necessary if you are executing an
            arithmetic operation. The "query" field must be the code operation you need to execute on the data file.

            - You MUST NOT provide code directly in the query field, INSTEAD you need to describe the operation you
            need to perform in natural language. The tool assistant will understand the query you provide and execute
            the operation based on it.

            To use this tool, you need to provide following fields 'VERY CAREFULLY':

            - [1] For "file_paths", provide a list of strings containing paths of the items you would like to execute
            the query on. You can at most provide 20 file paths in the list at once. If you think you need more than
            20 file paths, you can run the tool again later to provide rest of the files.

            - [2] For "query", provide the query you need to execute on the item, in "NATURAL LANGUAGE, ALWAYS".

                - **Example Queries:**
                    - "Please provide a summary of the image."
                    - "Please show the descriptive statistics of the file."
                    - "Please provide a chart based on the data in the file."

                - You always need to provide the queries in the "query" field, and in natural language.

            ---

            - **IMPORTANT NOTES:**

            - **NOTE**: The system will provide you the results in the next 'assistant' message. This message will
            have output of query execution, and you will be expected to take this response and provide an answer
            to user's question based on the response you received, in your own words. Think of this as an employee of
            yours that you are instructing to execute a query on a file, and you are expected to take the response
            of this employee and provide an answer to the user's question.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a direct link to user for reaching files, here is the base
                    URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'absolute' path by appending the
                file path to the base URL.

            ---

        """
    return response_prompt
