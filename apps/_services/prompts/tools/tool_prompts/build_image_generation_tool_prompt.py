from apps._services.tools.const import ToolTypeNames
from config.settings import BASE_URL


def build_structured_tool_prompt__image_generator():

    response_prompt = f"""
            **TOOL**: Image Generation Tool

            - The Image Generation Tool is a tool that allows you to generate images based on the prompts that you provide.
            You can use this tool to generate images based on the prompts that you provide, and the assistant will generate
            the images based on the prompts that you provide. You can use this tool to generate images for various use cases
            such as generating images for creative use cases, generating images for contents, and more.

            - The standardized format for the dictionary that you will output to use the Image Generation Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.IMAGE_GENERATION}",
                    "parameters": {{
                        "prompt": "...",
                        "size": "SQUARE" | "PORTRAIT" | "LANDSCAPE",
                        "quality": "STANDARD" | "HIGH_DEFINITION"
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "prompt" field should be the prompt that you would like to generate the image based on.
            The "image_size" field should be the size of the image that you would like to generate. The "quality" field
            should be the quality of the image that you would like to generate. The assistant will generate the image based
            on the prompt that you provide, the size of the image that you provide, and the quality of the image that you
            provide.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "prompt", provide the prompt that you would like to generate the image based on. You can provide the
            prompt in natural language, and the assistant will generate the image based on the prompt that you provide.

            2. For "image_size", provide the size of the image that you would like to generate. You can provide the size
            of the image as "SQUARE", "PORTRAIT", or "LANDSCAPE". The assistant will generate the image based on the size
            that you provide. If you fail to correctly specify one of these choices, the system will take SQUARE as the
            default value.

            3. For "quality", provide the quality of the image that you would like to generate. You can provide the quality
            of the image as "STANDARD" or "HIGH_DEFINITION". The assistant will generate the image based on the quality
            that you provide. If you fail to correctly specify one of these choices, the system will take STANDARD as the
            default value.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words. Think of this tool
            as an employee of yours that you are instructing to execute a query on a media item, and you are expected
            to take the response of this employee and provide an answer to the user's question based on the response
            that you receive from this employee.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {BASE_URL}
            - **NEVER, EVER:** provide a 'relative' path to the files. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """

    return response_prompt
