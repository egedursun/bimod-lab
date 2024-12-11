#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_file_system_data_source_prompt.py
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


def build_file_system_data_source_prompt(assistant: Assistant):
    from apps.datasource_file_systems.models import DataSourceFileSystem

    file_system_data_sources = DataSourceFileSystem.objects.filter(
        assistant=assistant
    )

    response_prompt = """
            ### **FILE SYSTEM CONNECTIONS (via SSH):**

            '''
            """

    for i, file_system_data_source in enumerate(file_system_data_sources):
        response_prompt += f"""
                [File System Data Source ID: {file_system_data_source.id}]
                    OS Type: {file_system_data_source.os_type}
                    File System Name: {file_system_data_source.name}
                    File System Description: {file_system_data_source.description or "N/A"}
                    Host URL: {file_system_data_source.host_url}
                    Port: {file_system_data_source.port or "N/A"}
                    Username: {file_system_data_source.username}
                    Maximum Records to Retrieve / Query (LIMIT): {file_system_data_source.os_read_limit_tokens}
                    Is Read Only: {file_system_data_source.is_read_only}
                    Schema of System:
                    '''

                        ##### YOUR FILE SYSTEM DIRECTORY SCHEMA SEARCH TOOL:

                            - You can use your SSH File System Directory Schema search tool to search and understand certain structures
                               within the database, by using your intuition at first to provide a reasonable query to search within
                               the schema, and then using the retrieved information, you can generate console commands/scripts to
                               manipulate the file system, read from the file system, analyze the data within a file system, and
                               use the data there in your response generation processes, as any operations requested by the user.

                            - Further instructions about how you can use the SSH File System directory schema search tool is
                            provided to you in the further sections of this prompt.

                    '''
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the File System Connections you have access. Keep these in mind while responding
            to user. If this part is EMPTY, it means that the user has not provided any File System Connections (yet),
            so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The system specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is not 100% handled by the system
            yet, so be careful with the number of records you retrieve per query, and always make sure you are within
            the retrieval limits specified.

            ##### **VERY IMPORTANT NOTE ABOUT 'FILE SYSTEM' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the file system of the server via an SSH client connection created in the
            background. You can use this to retrieve file system information, execute commands, and retrieve schema
            of the file system. Be careful with the commands you execute, as they can have a direct impact on the
            system. Stick very closely to the instructions provided by the user to avoid issues.

            #### **VERY IMPORTANT NOTE ABOUT 'read_only' FIELD:**
            - The 'is_read_only' field determines your ability to execute "write" operations on the system.
            If this field is set to 'True', you can only execute "read" operations. If this field is set to 'False',
            you can execute both "read" and "write" operations. Be very careful with the operations you execute
            on the system, as they can have a direct impact on the server.

            ---
            """

    return response_prompt


def build_semantor_file_system_data_source_prompt(temporary_sources: dict):
    file_system_data_sources = temporary_sources.get("data_sources").get("file_systems")

    response_prompt = """
            ### **FILE SYSTEM CONNECTIONS (via SSH):**

            '''
            """

    for i, file_system_data_source in enumerate(file_system_data_sources):
        response_prompt += f"""
                [File System Data Source ID: {file_system_data_source.id}]
                    OS Type: {file_system_data_source.os_type}
                    File System Name: {file_system_data_source.name}
                    File System Description: {file_system_data_source.description or "N/A"}
                    Host URL: {file_system_data_source.host_url}
                    Port: {file_system_data_source.port or "N/A"}
                    Username: {file_system_data_source.username}
                    Maximum Records to Retrieve / Query (LIMIT): {file_system_data_source.os_read_limit_tokens}
                    Is Read Only: {file_system_data_source.is_read_only}
                    Schema of System:
                    '''

                    ##### YOUR FILE SYSTEM DIRECTORY SCHEMA SEARCH TOOL:

                            - You can use your SSH File System Directory Schema search tool to search and understand certain structures
                               within the database, by using your intuition at first to provide a reasonable query to search within
                               the schema, and then using the retrieved information, you can generate console commands/scripts to
                               manipulate the file system, read from the file system, analyze the data within a file system, and
                               use the data there in your response generation processes, as any operations requested by the user.

                            - Further instructions about how you can use the SSH File System directory schema search tool is
                            provided to you in the further sections of this prompt.

                    '''
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the File System Connections you have access. Keep these in mind while responding
            to user. If this part is EMPTY, it means that the user has not provided any File System Connections (yet),
            so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The system specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is not 100% handled by the system
            yet, so be careful with the number of records you retrieve per query, and always make sure you are within
            the retrieval limits specified.

            ##### **VERY IMPORTANT NOTE ABOUT 'FILE SYSTEM' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the file system of the server via an SSH client connection created in the
            background. You can use this to retrieve file system information, execute commands, and retrieve schema
            of the file system. Be careful with the commands you execute, as they can have a direct impact on the
            system. Stick very closely to the instructions provided by the user to avoid issues.

            #### **VERY IMPORTANT NOTE ABOUT 'read_only' FIELD:**
            - The 'is_read_only' field determines your ability to execute "write" operations on the system.
            If this field is set to 'True', you can only execute "read" operations. If this field is set to 'False',
            you can execute both "read" and "write" operations. Be very careful with the operations you execute
            on the system, as they can have a direct impact on the server.

            ---
            """

    return response_prompt


def build_lean_file_system_data_source_prompt():
    response_prompt = """
            ### **FILE SYSTEM CONNECTIONS (via SSH):**

            '''
            <This information is redacted because you won't need it to serve your instructions.>

            '''

            ---

            #### **NOTE**: These are the File System Connections you have access. Keep these in mind while responding
            to user. If this part is EMPTY, it means that the user has not provided any File System Connections (yet),
            so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The system specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is not 100% handled by the system
            yet, so be careful with the number of records you retrieve per query, and always make sure you are within
            the retrieval limits specified.

            ##### **VERY IMPORTANT NOTE ABOUT 'FILE SYSTEM' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the file system of the server via an SSH client connection created in the
            background. You can use this to retrieve file system information, execute commands, and retrieve schema
            of the file system. Be careful with the commands you execute, as they can have a direct impact on the
            system. Stick very closely to the instructions provided by the user to avoid issues.

            #### **VERY IMPORTANT NOTE ABOUT 'read_only' FIELD:**
            - The 'is_read_only' field determines your ability to execute "write" operations on the system.
            If this field is set to 'True', you can only execute "read" operations. If this field is set to 'False',
            you can execute both "read" and "write" operations. Be very careful with the operations you execute
            on the system, as they can have a direct impact on the server.

            ---

            """

    return response_prompt
