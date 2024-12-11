#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_website_data_source_prompt.py
#  Last Modified: 2024-12-09 01:07:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 01:07:40
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

from apps.datasource_website.models import (
    DataSourceWebsiteStorageConnection,
    DataSourceWebsiteStorageItem
)


def build_website_data_source_prompt(assistant: Assistant):
    website_data_sources = DataSourceWebsiteStorageConnection.objects.filter(
        assistant=assistant
    )

    response_prompt = """
        ### **WEBSITE STORAGE CONNECTIONS:**

        '''
        """

    for i, website_data_source in enumerate(website_data_sources):
        website_data_source: DataSourceWebsiteStorageConnection

        website_items = website_data_source.storage_items.all()

        response_prompt += f"""
        [Websites Storage ID: {website_data_source.id}]
            Websites Storage Name: {website_data_source.name}
            DB Description: {website_data_source.description or "N/A"}
            Maximum Records to Retrieve / Query (LIMIT): {website_data_source.search_instance_retrieval_limit}
            Indexing Chunk Size and Overlap: {website_data_source.embedding_chunk_size} / {website_data_source.embedding_chunk_overlap}
            Website URLs in this Storage:
            '''
        """

        for j, website_item in enumerate(website_items):
            website_item: DataSourceWebsiteStorageItem

            response_prompt += f"""
            [{j}]: {website_item.website_url}
            """

        response_prompt += """
            '''

            '''
                ##### YOUR WEBSITE DATA SEARCH TOOL:

                - You can use your Website Data search tool to search and understand the contents of websites within the
                   website storages, by using your intuition at first to provide a reasonable query to search within
                   the websites, and then using the retrieved information, you can use the data in your response
                   generation processes to provide more accurate and relevant information to the user.

                - Further instructions about how you can use the Website Data search tool is provided to you in
                the further sections of this prompt.

            '''

    """

    response_prompt += """
        '''

        ---

        #### **NOTE**: These are the Website Storage Connections that you have access to. Keep these in mind while
        responding to user. All the website URLs and their content indexed within these storages are also provided for
        you, which you can use to choose which storage to search within (while using your website data search tool)
        If this part is EMPTY, it means that the user has not provided any Website Storages yet, so neglect this part.
        Or, if there are no website URLs indexed within the storage, it means that the user has not indexed any websites
        yet, so neglect this part.

        #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for vector retrievals while searching
        within the website data, specified as 'Maximum Records to Retrieve / Query (LIMIT)' field. While you are using
        your search tool, the search results will be delivered to you accordingly, along with the specifications
        of the chunk size and overlap for the indexing process.

        ---

        """

    return response_prompt


def build_semantor_website_data_source_prompt(temporary_sources: dict):
    website_data_sources = temporary_sources.get("data_sources").get("website_storages")

    response_prompt = """
            ### **WEBSITE STORAGE CONNECTIONS:**

            '''
            """

    for i, website_data_source in enumerate(website_data_sources):
        website_data_source: DataSourceWebsiteStorageConnection

        website_items = website_data_source.storage_items.all()

        response_prompt += f"""
            [Websites Storage ID: {website_data_source.id}]
                Websites Storage Name: {website_data_source.name}
                DB Description: {website_data_source.description or "N/A"}
                Maximum Records to Retrieve / Query (LIMIT): {website_data_source.search_instance_retrieval_limit}
                Indexing Chunk Size and Overlap: {website_data_source.embedding_chunk_size} / {website_data_source.embedding_chunk_overlap}
                Website URLs in this Storage:
                '''
            """

        for j, website_item in enumerate(website_items):
            website_item: DataSourceWebsiteStorageItem

            response_prompt += f"""
                [{j}]: {website_item.website_url}
                """

        response_prompt += """
                '''

                '''
                    ##### YOUR WEBSITE DATA SEARCH TOOL:

                    - You can use your Website Data search tool to search and understand the contents of websites within the
                       website storages, by using your intuition at first to provide a reasonable query to search within
                       the websites, and then using the retrieved information, you can use the data in your response
                       generation processes to provide more accurate and relevant information to the user.

                    - Further instructions about how you can use the Website Data search tool is provided to you in
                    the further sections of this prompt.

                '''

        """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Website Storage Connections that you have access to. Keep these in mind while
            responding to user. All the website URLs and their content indexed within these storages are also provided for
            you, which you can use to choose which storage to search within (while using your website data search tool)
            If this part is EMPTY, it means that the user has not provided any Website Storages yet, so neglect this part.
            Or, if there are no website URLs indexed within the storage, it means that the user has not indexed any websites
            yet, so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for vector retrievals while searching
            within the website data, specified as 'Maximum Records to Retrieve / Query (LIMIT)' field. While you are using
            your search tool, the search results will be delivered to you accordingly, along with the specifications
            of the chunk size and overlap for the indexing process.

            ---

            """

    print(response_prompt)

    return response_prompt


def build_lean_website_data_source_prompt():
    response_prompt = """
        ### **WEBSITE STORAGE CONNECTIONS:**

        '''
        <This data is redacted because you won't need it to serve your instructions.>
        '''

        ---

        #### **NOTE**: These are the Website Storage Connections that you have access to. Keep these in mind while
        responding to user. All the website URLs and their content indexed within these storages are also provided for
        you, which you can use to choose which storage to search within (while using your website data search tool)
        If this part is EMPTY, it means that the user has not provided any Website Storages yet, so neglect this part.
        Or, if there are no website URLs indexed within the storage, it means that the user has not indexed any websites
        yet, so neglect this part.

        #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for vector retrievals while searching
        within the website data, specified as 'Maximum Records to Retrieve / Query (LIMIT)' field. While you are using
        your search tool, the search results will be delivered to you accordingly, along with the specifications
        of the chunk size and overlap for the indexing process.

        ---

        """

    return response_prompt
