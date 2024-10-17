#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_image_modification_tool_prompt.py
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


def build_tool_prompt__edit_image():
    response_prompt = f"""
            ### **TOOL**: Image Modification Tool

            - The Image Modification Tool is a tool allows you to modify images based on the prompts you provide.
            You can use this to modify images based on prompts, and the assistant will modify the images based on them.
            You can use this to modify images for various use cases such as for creative use cases, for content
            generations, and more.

            - The format for the dictionary you will output to use the Image Modification Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_EDIT_IMAGE}",
                    "parameters": {{
                        "prompt": "...",
                        "edit_image_uri": "...",
                        "edit_image_mask_uri": "...",
                        "image_size": "SQUARE" | "PORTRAIT" | "LANDSCAPE"
                    }}
                }}
            '''

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "prompt" field is the prompt you would like to modify the image based on.
            The "edit_image_uri" should be URI of the image that you need to edit. The "edit_image_mask_uri" field
            is the URI of the mask image that represents the area that needs to be edited within the edit image.
            The "image_size" is the size of the image that you need to modify. The agent will modify the image
            based on the prompt, the edit image, the mask image, and the size of the image supplied. If you don't
            provide, or fail to correctly specify one of the valid choices, the system will take SQUARE as the
            default value for the image size.

            To use this tool, you need to provide following fields 'VERY CAREFULLY':

            - [1] For "prompt", provide the prompt you need to modify the image based on. You can provide this in
            natural language, and the tool agent will modify the image accordingly.

            - [2] For "edit_image_uri", provide the URI of the image you need to edit.

            - [3] For "edit_image_mask_uri", provide the URI of the mask image that represents the area needs to be
            edited within the edit image.

            - [4] For "image_size", provide the size of the image that you need to modify. You can provide the size
            of the image as "SQUARE", "PORTRAIT", or "LANDSCAPE". The tool agent will modify the image based on the
            size you provided. If you fail to correctly specify one of these choices, the system will take SQUARE
            as the default value.

            ---

            #### **IMPORTANT NOTES:**

            - **ABOUT INPUTS**: The image uri's representing the edit image and the mask image will be shared with
            prefixes representing their role:

                - [1] If the name of the image URI starts with
                    '''edit_image__original_version__''', it represents the ORIGINAL version of the image you need
                        to edit.
                - [2] If the name of the image URI starts with
                    '''edit_image__masked_version__''', it represents the MASKED version of the image with the area
                    needs to be edited as masked out in the image.

            - **NOTE**: The system will provide you the results in the next 'assistant' message. This message will
            have the output of the execution, and you will be expected to take this and provide an answer
            to user's question based on the response you receive, in your own words. Think of this tool as an employee
            that you are instructing to execute a query on an image, and you are expected to take the response of the
            employee and provide an answer to user's question based on it.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a direct URL or link to user for reaching files, here is the base
                    URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'absolute' path by appending
                file path to base URL.

        """
    return response_prompt
