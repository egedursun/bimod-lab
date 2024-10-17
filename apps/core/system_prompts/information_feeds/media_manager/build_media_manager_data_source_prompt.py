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
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection


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
                    Storage Description: {media_storage_data_source.description}
                    File Category: {media_storage_data_source.media_category}

                    #### *Names and Descriptions of the Media Items:*
                """
        media_items = media_storage_data_source.items.all()
        for j, media_item in enumerate(media_items):
            response_prompt += f"""
                    - [Media Item ID: {media_item.id}]
                        File Name: {media_item.media_file_name}
                        Description: {media_item.description}
                        Size: {media_item.media_file_size}
                        File Type: {media_item.media_file_type}
                        File Path: {media_item.full_file_path}
                        Created At: {media_item.created_at}

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
