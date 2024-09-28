from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection


def build_storage_data_source_prompt(assistant: Assistant):
    # Gather the File System datasource connections of the assistant
    media_storage_data_sources = DataSourceMediaStorageConnection.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
            **MEDIA STORAGE RESOURCE CONNECTIONS:**

            '''
            """

    for i, media_storage_data_source in enumerate(media_storage_data_sources):
        response_prompt += f"""
                [Media Storage Data Source ID: {media_storage_data_source.id}]
                    Media Storage Name: {media_storage_data_source.name}
                    Media Storage Description: {media_storage_data_source.description}
                    Media Category: {media_storage_data_source.media_category}

                    *Names and Descriptions of the Media Items:*
                """

        media_items = media_storage_data_source.items.all()
        for j, media_item in enumerate(media_items):
            response_prompt += f"""
                    - [Media Item ID: {media_item.id}]
                        File Name: {media_item.media_file_name}
                        Description: {media_item.description}
                        File Size: {media_item.media_file_size}
                        Media File Type: {media_item.media_file_type}
                        Full File Path: {media_item.full_file_path}
                        Created At: {media_item.created_at}

                """

    response_prompt += """
            -------

            '''

            **NOTE**: These are the Media Storage Resource Connections you have access to. Make sure to keep these in
             mind while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Media Storage Resource Connections (yet), so neglect this part if that is the case.

            **VERY IMPORTANT NOTE ABOUT 'MEDIA STORAGE' DATA SOURCES / CONNECTIONS:**
            - This is a direct connection to the media storage of the server. You can use this connection to retrieve
            media information, ask queries and questions about the media, and retrieve information regarding them;
            additionally you can build queries to generate charts, interpret images, describe an algorithm / goal
            to be executed with a code interpreter.

            **HOW YOUR QUERIES ARE BEING PROCESSED:**
            - Your queries along with the file paths you have given will be send to a distinct GPT assistant which
            will process the queries and provide you with the results. The results will be displayed in the
            response of the assistant, along with the URIs of the generated files, if any.

            -------
            """

    return response_prompt


def build_lean_storage_data_source_prompt():
    # Build the prompt
    response_prompt = """
            **MEDIA STORAGE RESOURCE CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            **NOTE**: These are the Media Storage Resource Connections you have access to. Make sure to keep these in
             mind while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Media Storage Resource Connections (yet), so neglect this part if that is the case.

            **VERY IMPORTANT NOTE ABOUT 'MEDIA STORAGE' DATASOURCES:**
            - This is a direct connection to the media storage of the server. You can use this connection to retrieve
            media information, ask queries and questions about the media, and retrieve information regarding them;
            additionally you can build queries to generate charts, interpret images, describe an algorithm / goal
            to be executed with a code interpreter.

            **HOW YOUR QUERIES ARE BEING PROCESSED:**
            - Your queries along with the file paths you have given will be send to a distinct GPT assistant which
            will process the queries and provide you with the results. The results will be displayed in the
            response of the assistant, along with the URIs of the generated files, if any.

            -------
    """
    return response_prompt
