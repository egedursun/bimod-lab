from apps._services.tools.const import ToolTypeNames
from config.settings import MEDIA_URL


def build_structured_tool_prompt__image_modification():
    response_prompt = f"""
            **TOOL**: Image Modification Tool

            - The Image Modification Tool is a tool that allows you to modify images based on the prompts that you provide.
            You can use this tool to modify images based on the prompts that you provide, and the assistant will modify
            the images based on the prompts that you provide. You can use this tool to modify images for various use cases
            such as modifying images for creative use cases, modifying images for content generations, and more.

            - The standardized format for the dictionary that you will output to use the Image Modification Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.IMAGE_MODIFICATION}",
                    "parameters": {{
                        "prompt": "...",
                        "edit_image_uri": "...",
                        "edit_image_mask_uri": "...",
                        "image_size": "SQUARE" | "PORTRAIT" | "LANDSCAPE"
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "prompt" field should be the prompt that you would like to modify the image based on.
            The "edit_image_uri" field should be the URI of the image that you need to edit. The "edit_image_mask_uri" field
            should be the URI of the mask image that basically represents the area that needs to be edited within the
            edit image. The "image_size" field should be the size of the image that you would like to modify. The assistant
            will modify the image based on the prompt that you provide, the image that you provide, the mask image that you
            provide, and the size of the image that you provide. If you don't provide, or fail to correctly specify one of
            these choices, the system will take SQUARE as the default value for the image size.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "prompt", provide the prompt that you would like to modify the image based on. You can provide the
            prompt in natural language, and the assistant will modify the image based on the prompt that you provide.

            2. For "edit_image_uri", provide the URI of the image that you need to edit. You can provide the URI of the
            image that you need to edit. The assistant will modify the image based on the image that you provide.

            3. For "edit_image_mask_uri", provide the URI of the mask image that basically represents the area that needs
            to be edited within the edit image. You can provide the URI of the mask image that you need to use to edit the
            image. The assistant will modify the image based on the mask image that you provide.

            4. For "image_size", provide the size of the image that you would like to modify. You can provide the size
            of the image as "SQUARE", "PORTRAIT", or "LANDSCAPE". The assistant will modify the image based on the size
            that you provide. If you fail to correctly specify one of these choices, the system will take SQUARE as the
            default value.

            ---

            **IMPORTANT NOTES:**

            **ABOUT INPUTS**: The image uri's representing the edit image and the mask image will be shared with you with prefixes
            representing their role:
            1. If the name of the image URI starts with
                '''edit_image__original_version__''', it represents the ORIGINAL version of the image that you need to edit.
            2. If the name of the image URI starts with
                '''edit_image__masked_version__''', it represents the masked version of the image with the area that
                needs to be edited masked out in the image.

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
