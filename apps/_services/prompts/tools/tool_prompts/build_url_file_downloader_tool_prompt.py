from apps._services.tools.const import ToolTypeNames
from config.settings import BASE_URL


def build_structured_tool_prompt__url_file_downloader():

    response_prompt = f"""
            **TOOL**: URL File Downloader

            - The URL File Downloader Tool is a tool you can use to download files from the internet by providing
            the URL of the file that you would like to download. This URL could either be provided by the user
            in terms of a direct link to the file within your conversation, or it could be a URL that you have
            found on the internet that you would like to download the file from (if you have a browsing tool to
            connect to the internet).

            - The standardized format for the dictionary that you will output to use the URL File Downloader Tool
            is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.URL_FILE_DOWNLOADER}",
                    "parameters": {{
                        "media_storage_connection_id": "...",
                        "url": "..."
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "media_storage_connection_id" field should be the ID of the media storage connection
            that you would like to download the file to, and the "url" field should be the URL of the file that you
            would like to download. The system will download the file from the URL and store it in the media storage
            connection that you have provided, and return you the full path of the file that is downloaded.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "media_storage_connection_id", provide the ID of the media storage connection that you would like
            to execute the query on.

            2. For "url", provide the URL of the file that you would like to download. This URL could either be
            provided by the user in terms of a direct link to the file within your conversation, or it could be a URL
            that you have found on the internet that you would like to download the file from. ONLY send a "SINGLE"
            URL in the "url" field, NEVER provide a "LIST" of URLs. If you think you need to download more than one
            file, you can run the tool again to download more files.

            ---

            **IMPORTANT NOTES:**

            - While you are providing the connection ID, make sure you are passing an adequate connection ID that
            is suitable for the "media category" you are aiming to download. For example, if you are downloading an
            image, make sure you are providing a connection ID that is suitable for storing images, and if you are
            providing a code file, make sure you are providing a connection ID that is suitable for storing code files,
            and so on.

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the full URL of the file that is downloaded and stored in the media storage connection that you have
            provided. You can use this URL to either show it directly in Markdown format, or provide a direct link for
            the full path of the file.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the file or images, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {BASE_URL}
            - **NEVER, EVER:** provide a 'relative' path to the file or image. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """

    return response_prompt
