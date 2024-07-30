from apps._services.tools.const import ToolTypeNames
from config.settings import BASE_URL


def build_structured_tool_prompt__image_variation():

    response_prompt = f"""
            **TOOL**: Image Variation Tool

            - The Image Variation Tool is a tool that allows you to create variations of images based on the image that
            you provide. You can use this tool to create variations of images based on the image that you provide, and
            the assistant will create variations of the image based on the image that you provide.

            - The standardized format for the dictionary that you will output to use the Image Variation Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.IMAGE_VARIATION}",
                    "parameters": {{
                        "image_uri": "...",
                        "image_size": "SQUARE" | "PORTRAIT" | "LANDSCAPE"
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "image_uri" field should be the URI of the image that you need to create variations of.
            The "image_size" field should be the size of the image that you would like to create variations of. The assistant
            will create variations of the image based on the image that you provide and the size of the image that you provide.
            If you don't provide, or fail to correctly specify one of these choices, the system will take SQUARE as the
            default value for the image size.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "image_uri", provide the URI of the image that you need to create variations of. You can provide the
            URI of the image that you need to create variations of. The assistant will create variations of the image based
            on the image that you provide.

            2. For "image_size", provide the size of the image that you would like to create variations of. You can provide
            the size of the image as "SQUARE", "PORTRAIT", or "LANDSCAPE". The assistant will create variations of the image
            based on the size that you provide. If you fail to correctly specify one of these choices, the system will take
            SQUARE as the default value.

            ---

            **IMPORTANT NOTES:**

            **ABOUT INPUTS**: This tool does not allow you to provide any prompt for creating variations of the image.
            You only need to provide the URI of the image that you need to create variations of and the size of the image
            that you would like to create variations of. The assistant will create variations of the image based on the
            image that you provide and the size of the image that you provide.

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
