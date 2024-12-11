#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: retrieval_via_http_client_tool_prompt.py
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


def build_tool_prompt__retrieval_via_http_client():
    response_prompt = f"""

            ### **TOOL**: URL File Downloader

            - The URL File Downloader Tool is a tool you can use to download files from internet by providing
            URL of the file that you need to download. This URL can either be provided by user in terms of a direct
            link to file within your conversation, or it could be a URL that you found on the internet you would like
            to download the file from (if you have a browsing tool to connect to the internet).

            - The format for dictionary you will output to use URL File Downloader Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_HTTP_RETRIEVAL}",
                    "parameters": {{
                        "media_storage_connection_id": "...",
                        "url": "..."
                    }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "media_storage_connection_id" must be the ID of media storage connection
            you would like to download file to, and "url" field must be URL of the file that you want to download.
            The system will download the file from URL and store it in the media storage connection you have provided,
            and return you full path of the file that is downloaded.

            To use this, you need to provide the following field 'VERY CAREFULLY':

            - [1] For "media_storage_connection_id", provide ID of the media storage connection you would like
            to execute the query on and the file is going to be saved to.

            - [2] For "url", provide URL of the file you would like to download. This URL can either be provided by
            user in terms of a direct link to file within your conversation, or it can be a URL that you found on
            internet you would like to download the file from.

            ---

            - ONLY send a "SINGLE" URL in the "url" field, NEVER provide a "LIST" of URLs. If you think you need to
            download more than one file, you can run the tool again later to download more.

            ---

            #### **IMPORTANT NOTES:**

            - While you are providing the connection ID, make sure you are passing an adequate connection ID that
            is suitable for the "media category" you are aiming to download. For example, if you are downloading an
            image, make sure you are providing a connection ID suitable for storing images, and if you are
            providing a code file, make sure you are providing a connection ID suitable for storing code files,
            and so on...

            - **NOTE**: The system will provide you with results in next 'assistant' message. This message will
            have the full URL of file that is downloaded and stored in the media storage connection you have
            specified. You can use the URL to either show it directly in Markdown format, or provide a link for
            the full path of it.

            ---

            #### **ABOUT PROVIDING URLS & LINKS:**
            - If you need to provide a direct link to user for reaching files or images, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to files or images. Always provide 'absolute' path by
            appending the file path to the base URL.

            ---

        """

    return response_prompt
