#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_image_variation_tool_prompt.py
#  Last Modified: 2024-10-05 02:26:00
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


def build_tool_prompt__dream_image():
    response_prompt = f"""
            ### **TOOL**: Image Variation Tool

            - The Image Variation Tool is a tool that allows you to create variations of images based on the image you
            provide. The tool assistant will create these image variations for you.

            - The format for the dictionary you will output to use the Image Variation Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_DREAM_IMAGE}",
                    "parameters": {{
                        "image_uri": "...",
                        "image_size": "SQUARE" | "PORTRAIT" | "LANDSCAPE"
                    }}
                }}
            '''

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "image_uri" field should be the URI of the image you need to create variations.
            The "image_size" should be the size of the image you would like to create variations of.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            - [1] For "image_uri", provide the URI of the image you need to create variations.

            - [2] For "image_size", provide the size of the image you need to create variations. You can provide the
                    size of the image as "SQUARE", "PORTRAIT", or "LANDSCAPE". If you fail to correctly specify
                    one of these choices, the system will take SQUARE as the default value.

            ---

            #### **IMPORTANT NOTES:**

            - **ABOUT INPUTS**: This tool does not allow you to provide any prompt for creating variations. You only
            need to provide the URI of the image you need to create variations and the size of the image. The
            assistant will create variations based on the parameters you have given.

            - **NOTE**: The system will provide you the results in the next 'assistant' message. This message will
            have the output of the execution, and you will be expected to take this and provide an answer to user's
            question based on the response you received, in your own words. Think of this tool as an employee that
            you are instructing to execute a query on an image, and you are expected to take the response of the
            employee and provide an answer to user's question using it.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a URL or link to the user for reaching files or images, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an ABSOLUTE HTTP URL reference to file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' URL or path to the files. Always provide 'absolute' path/URL
                    by appending the file path to the BASE URL.

        """
    return response_prompt
