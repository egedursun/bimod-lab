from django.contrib.auth.models import User

from apps.assistants.models import Assistant
from apps.datasource_file_systems.models import DataSourceFileSystem


def build_file_system_datasource_prompt(assistant: Assistant, user: User):

    response_prompt = ""
    # Gather the File System datasource connections of the assistant
    file_system_datasources = DataSourceFileSystem.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
            **FILE SYSTEM CONNECTIONS (via SSH):**

            '''
            """

    for i, file_system_datasource in enumerate(file_system_datasources):
        response_prompt += f"""
                [File System Datasource ID: {file_system_datasource.id}]
                    Operating System Type: {file_system_datasource.os_type}
                    File System Name: {file_system_datasource.name}
                    File System Description: {file_system_datasource.description}
                    Host URL: {file_system_datasource.host_url}
                    Port: {file_system_datasource.port}
                    Username: {file_system_datasource.username}
                    Maximum Records to Retrieve per Query (LIMIT): {file_system_datasource.os_read_limit_tokens}
                    Is Read Only: {file_system_datasource.is_read_only}
                    Schema of the File System: {file_system_datasource.file_directory_tree}
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

            **VERY IMPORTANT NOTE ABOUT 'FILE SYSTEM' DATASOURCES:**
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
