#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: build_file_system_data_source_prompt.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:09:49
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps.assistants.models import Assistant
from apps.datasource_file_systems.models import DataSourceFileSystem


def build_file_system_data_source_prompt(assistant: Assistant):
    # Gather the File System datasource connections of the assistant
    file_system_data_sources = DataSourceFileSystem.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
            **FILE SYSTEM CONNECTIONS (via SSH):**

            '''
            """

    for i, file_system_data_source in enumerate(file_system_data_sources):
        response_prompt += f"""
                [File System Data Source ID: {file_system_data_source.id}]
                    Operating System Type: {file_system_data_source.os_type}
                    File System Name: {file_system_data_source.name}
                    File System Description: {file_system_data_source.description}
                    Host URL: {file_system_data_source.host_url}
                    Port: {file_system_data_source.port}
                    Username: {file_system_data_source.username}
                    Maximum Records to Retrieve per Query (LIMIT): {file_system_data_source.os_read_limit_tokens}
                    Is Read Only: {file_system_data_source.is_read_only}
                    Schema of the File System: {file_system_data_source.file_directory_tree}
                """

    response_prompt += """
            -------

            '''

            **NOTE**: These are the File System Connections you have access to. Make sure to keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any File System Connections (yet), so neglect this part if that is the case.

            **NOTE about RETRIEVAL LIMITS**: The system has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is not 100% handled by the system
            yet, so be careful with the number of records you retrieve per query, and always make sure you
            are within the retrieval limits specified by the user.

            **VERY IMPORTANT NOTE ABOUT 'FILE SYSTEM' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the file system of the server via an SSH client connection created in the
            background for your use. You can use this connection to retrieve file system information, execute commands,
            and retrieve the schema of the file system. Be careful with the commands you execute, as they can have
            a direct impact on the file system of the server. Stick very closely to the instructions provided by the
            user to avoid any issues.

            **VERY IMPORTANT NOTE ABOUT 'read_only' FIELD:**
            - The 'is_read_only' field determines your ability to execute "write" operations on the file system.
            If this field is set to 'True', you can only execute "read" operations. If this field is set to 'False',
            you can execute both "read" and "write" operations. Be very careful with the operations you execute
            on the file system, as they can have a direct impact on the file system of the server.

            -------
            """

    return response_prompt


def build_lean_file_system_data_source_prompt():
    # Build the prompt
    response_prompt = """
            **FILE SYSTEM CONNECTIONS (via SSH):**

            '''
            <This information is redacted because you won't need it to serve your instructions.>

            '''

            **NOTE**: These are the File System Connections you have access to. Make sure to keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any File System Connections (yet), so neglect this part if that is the case.

            **NOTE about RETRIEVAL LIMITS**: The system has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is not 100% handled by the system
            yet, so be careful with the number of records you retrieve per query, and always make sure you
            are within the retrieval limits specified by the user.

            **VERY IMPORTANT NOTE ABOUT 'FILE SYSTEM' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the file system of the server via an SSH client connection created in the
            background for your use. You can use this connection to retrieve file system information, execute commands,
            and retrieve the schema of the file system. Be careful with the commands you execute, as they can have
            a direct impact on the file system of the server. Stick very closely to the instructions provided by the
            user to avoid any issues.

            **VERY IMPORTANT NOTE ABOUT 'read_only' FIELD:**
            - The 'is_read_only' field determines your ability to execute "write" operations on the file system.
            If this field is set to 'True', you can only execute "read" operations. If this field is set to 'False',
            you can execute both "read" and "write" operations. Be very careful with the operations you execute
            on the file system, as they can have a direct impact on the file system of the server.

            -------
            """

    return response_prompt
