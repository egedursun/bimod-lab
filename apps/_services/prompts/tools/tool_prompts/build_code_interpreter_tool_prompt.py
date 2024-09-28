from apps._services.tools.utils import ToolTypeNames
from config.settings import MEDIA_URL


def build_structured_tool_prompt__code_interpreter():
    response_prompt = f"""
            **TOOL**: Code Interpreter Tool

            - The Code Interpreter Tool is a tool that allows you to write and execute code operations in an integrated
            Python environment. You can use this tool to write code operations that you would like to execute, and the
            assistant will execute the code operation and provide you with the results. You can use this tool to write
            code operations that you would like to execute on a specific data file. Unlike the Media Storage Query
            Execution Tool, the Code Interpreter Tool is a dedicated tool for writing and executing code operations
            for various use cases such as arithmetic operations, unit conversions, sensitive calculations, and more.

            - The standardized format for the dictionary that you will output to use the Code Interpreter Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.CODE_INTERPRETER}",
                    "parameters": {{
                        "file_paths": ["...", "...", "..."],
                        "query": "..."
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "file_paths" field should be a list of strings that contain the paths of the data files
            that you would like to execute the code operation on. You don't have to provide a file path if you don't want
            to execute the code operation on a data file. For example, this wouldn't be necessary if you are executing an
            arithmetic operation. The "query" field should be the code operation that you would like to execute on the
            data file. You must not provide the code directly in the query field, instead you need to simply describe
            the operation that you would like to perform in natural language. The assistant will understand the query
            that you provide and execute the code operation based on the query that you provide.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "file_paths", provide a list of strings that contain the paths of the media items that you would
            like to execute the query on. You can at most provide 20 file paths in the list at once. If you think you
            need to provide more than 20 file paths, you can run the tool again to provide more file paths.

            2. For "query", provide the query that you would like to execute on the media item, in NATURAL LANGUAGE,
            ALWAYS.
                - *Example Queries:*
                    - "Please provide a summary of the image."
                    - "Please show the descriptive statistics of the file."
                    - "Please provide a chart based on the data in the file."
                - You always need to provide the queries in the "query" field, and in natural language.

            ---

            **IMPORTANT NOTES:**

            - For file interpretations, you will receive three fields in the output; the textual outputs for
            representing the response of the query, the file URIs for representing the URIs of the files that are
            generated as a result of the query.

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words. Think of this tool
            as an employee of yours that you are instructing to execute a query on a media item, and you are expected
            to take the response of this employee and provide an answer to the user's question based on the response
            that you receive from this employee.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to the files. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """
    return response_prompt
