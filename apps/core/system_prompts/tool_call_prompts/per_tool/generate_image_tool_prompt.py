#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_image_generation_tool_prompt.py
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


from apps.core.tool_calls.utils import ToolCallDescriptorNames
from config.settings import MEDIA_URL


def build_tool_prompt__generate_image():
    response_prompt = f"""
            ### **TOOL**: Image Generation Tool

            - The Image Generation Tool is a tool allows you to generate images based on prompts you provide.
            You can use this to generate images based on prompts, and tool assistant will generate images based on
            them. You can use this to generate images for various use cases such as for creative use cases, for
            contents, and more.

            - The format for the dictionary you will output to use Image Generation Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_GENERATE_IMAGE}",
                    "parameters": {{
                        "prompt": "...",
                        "size": "SQUARE" | "PORTRAIT" | "LANDSCAPE",
                        "quality": "STANDARD" | "HIGH_DEFINITION"
                    }}
                }}
            '''

            ---

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "prompt" must be the prompt you need to generate image based on. The "image_size"
            must be size of the image you would like to generate. The "quality" must be quality of image you need to
            generate. The agent will generate the image based on prompt you provided, as well as the size of the image,
            and quality of image.

            To use this, you need to provide the following fields 'VERY CAREFULLY':

            - [1] For "prompt", provide prompt you need to generate image based on. You can provide prompt in
            natural language, and the tool assistant will generate the image based on that.

            - [2] For "image_size", provide size of the image you want to generate. You can provide the size
            of the image as "SQUARE", "PORTRAIT", or "LANDSCAPE". The assistant will generate image based on the size
            that you provided. If you fail to correctly specify one of these choices, the system will take SQUARE as
            default value.

            - [3] For "quality", provide quality of image you want to generate. You can provide quality of image as
            "STANDARD" or "HIGH_DEFINITION". The tool assistant will generate image based on the quality you provided.
            If you fail to correctly specify one of these choices, the system will take STANDARD as default value.

            ---

            #### **IMPORTANT NOTES:**

            - **NOTE**: The system will provide you the results in next 'assistant' message. This message will
            have output of execution, and you will be expected to take this response and provide an answer
            to user's question, in your own words. Think of this as an employee you are instructing to execute a query
            on a media item, and you are expected to take the response of this employee and provide an answer to
            user's question.

            #### **ABOUT PROVIDING URLS & LINKS:**

            - If you need to provide a direct link to user for reaching files, here is base
                URL you need to 'DIRECTLY' append file path to provide an absolute HTTP URL to file:
                - {MEDIA_URL}

            - **NEVER, EVER:** provide a 'relative' path to files. Always provide the 'absolute' path by
            appending file path to the base URL.

            ---

        """
    return response_prompt
