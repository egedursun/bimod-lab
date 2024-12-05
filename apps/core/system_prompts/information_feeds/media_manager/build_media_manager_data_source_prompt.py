#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_storage_data_source_prompt.py
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


from apps.assistants.models import Assistant

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection
)


def build_media_manager_data_source_prompt(assistant: Assistant):
    media_manager_data_sources = DataSourceMediaStorageConnection.objects.filter(assistant=assistant)
    response_prompt = """
            ### **MEDIA STORAGE RESOURCE CONNECTIONS:**

            '''
            """

    for i, media_storage_data_source in enumerate(media_manager_data_sources):
        response_prompt += f"""
                [Media Storage Data Source ID: {media_storage_data_source.id}]
                    Storage Name: {media_storage_data_source.name}
                    Storage Description: {media_storage_data_source.description or "N/A"}
                    File Category: {media_storage_data_source.media_category}

                    #### *Format of the Results when you search for Media Items in a Storage:*
                    - [media_item_id: <id of the item> ]
                        media_file_name: <file name of the media item>
                        media_file_description: <description of the media file item>
                        media_file_size: <size of the media file item>
                        media_file_type: <type (format) of the media file item
                        media_file_path: <the file path of the item (you can use to download the item if required)>
                        media_file_created_at: <the items creation date>

                   ##### YOUR MEDIA ITEM SEARCH TOOL:

                   - You can use your media item search tool to search for media items in a media storage, and then using
                   the retrieved information, you can download the media items, analyze them, and use them in your
                   response generation processes (such as if the user requires you to analyze a specific CSV file, or
                   asks for you to unzip a compressed file, or provides an image file and asks what is in the image,
                   etc.)

                   - Further instructions about how you must use the media item search tool is provided to you in the
                   further sections of this prompt.

                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Media Storage Resource Connections you have access. Keep these in mind while
            responding to the user. If this part is EMPTY, it means that the user has not provided any Media Storage
            Resource Connections (yet), so neglect this part.

            #### **IMPORTANT NOTE ABOUT 'MEDIA STORAGE' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the media storage of the server. You can use this to retrieve
            media info/metadata, ask queries and questions about the media, and retrieve info regarding them;
            AND you can build queries to generate charts, interpret images, describe an algorithm / goal
            to be executed with a sandbox interpreter.

            #### **HOW YOUR QUERIES ARE PROCESSED:**
            - Your queries along with the file paths you give will be send to a distinct agent which will process
            the queries and provide you the results. The results will be displayed in the response of the agent,
            along with the URIs of the generated files, if any.

            ---
            """

    return response_prompt


def build_semantor_media_manager_data_source_prompt(temporary_sources: dict):
    media_manager_data_sources = temporary_sources.get("data_sources").get("media_storages")

    response_prompt = """
            ### **MEDIA STORAGE RESOURCE CONNECTIONS:**

            '''
            """

    for i, media_storage_data_source in enumerate(media_manager_data_sources):
        response_prompt += f"""
            [Media Storage Data Source ID: {media_storage_data_source.id}]
                Storage Name: {media_storage_data_source.name}
                Storage Description: {media_storage_data_source.description or "N/A"}
                File Category: {media_storage_data_source.media_category}

               #### *Format of the Results when you search for Media Items in a Storage:*
                - [media_item_id: <id of the item> ]
                    media_file_name: <file name of the media item>
                    media_file_description: <description of the media file item>
                    media_file_size: <size of the media file item>
                    media_file_type: <type (format) of the media file item
                    media_file_path: <the file path of the item (you can use to download the item if required)>
                    media_file_created_at: <the items creation date>

               ##### YOUR MEDIA ITEM SEARCH TOOL:

               - You can use your media item search tool to search for media items in a media storage, and then using
               the retrieved information, you can download the media items, analyze them, and use them in your
               response generation processes (such as if the user requires you to analyze a specific CSV file, or
               asks for you to unzip a compressed file, or provides an image file and asks what is in the image,
               etc.)

               - Further instructions about how you must use the media item search tool is provided to you in the
               further sections of this prompt.

        """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Media Storage Resource Connections you have access. Keep these in mind while
            responding to the user. If this part is EMPTY, it means that the user has not provided any Media Storage
            Resource Connections (yet), so neglect this part.

            #### **IMPORTANT NOTE ABOUT 'MEDIA STORAGE' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the media storage of the server. You can use this to retrieve
            media info/metadata, ask queries and questions about the media, and retrieve info regarding them;
            AND you can build queries to generate charts, interpret images, describe an algorithm / goal
            to be executed with a sandbox interpreter.

            #### **HOW YOUR QUERIES ARE PROCESSED:**
            - Your queries along with the file paths you give will be send to a distinct agent which will process
            the queries and provide you the results. The results will be displayed in the response of the agent,
            along with the URIs of the generated files, if any.

            ---
            """

    return response_prompt


def build_lean_media_manager_data_source_prompt():
    response_prompt = """
            ### **MEDIA STORAGE RESOURCE CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            ---

            #### **NOTE**: These are the Media Storage Resource Connections you have access. Keep these in mind while
            responding to the user. If this part is EMPTY, it means that the user has not provided any Media Storage
            Resource Connections (yet), so neglect this part.

            #### **IMPORTANT NOTE ABOUT 'MEDIA STORAGE' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the media storage of the server. You can use this to retrieve
            media info/metadata, ask queries and questions about the media, and retrieve info regarding them;
            AND you can build queries to generate charts, interpret images, describe an algorithm / goal
            to be executed with a sandbox interpreter.

            #### **HOW YOUR QUERIES ARE PROCESSED:**
            - Your queries along with the file paths you give will be send to a distinct agent which will process
            the queries and provide you the results. The results will be displayed in the response of the agent,
            along with the URIs of the generated files, if any.

            ---
    """
    return response_prompt
