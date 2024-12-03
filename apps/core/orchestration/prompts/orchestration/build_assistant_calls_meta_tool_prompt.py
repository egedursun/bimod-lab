#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_assistant_calls_meta_tool_prompt.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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
from apps.orchestrations.models import Maestro
from config.settings import MEDIA_URL
from apps.assistants.models import Assistant

from apps.datasource_sql.models import (
    SQLDatabaseConnection,
    CustomSQLQuery
)

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection,
    DataSourceMediaStorageItem
)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection
)

from apps.datasource_file_systems.models import (
    DataSourceFileSystem
)

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection,
    DataSourceMLModelItem
)

from apps.datasource_browsers.models import (
    DataSourceBrowserConnection
)

from apps.mm_functions.models import (
    CustomFunctionReference,
    CustomFunction
)

from apps.mm_apis.models import (
    CustomAPIReference,
    CustomAPI
)

from apps.mm_scripts.models import (
    CustomScriptReference,
    CustomScript
)


def build_orchestration_structured_tool_usage_instructions_prompt(maestro):
    response_prompt = f"""
        **WORKER TOOL USAGE ABILITY:** (Very important! - Make sure to UNDERSTAND this part well)

        - As an orchestration assistant, you are able to use worker assistants to provide better and more accurate
        responses to the user's questions when you believe that there would be a benefit in doing so.

        - While you are answering user's questions, you have two options:

            1. You can directly provide a response to the question by text: Do this if you think you have enough
            information to provide an answer to the user's question with the data you currently have. These
            responses must be delivered in natural language.

            2. You can output a JSON file, which will be interpreted by the system as a request to use a 'WORKER TOOL'.
                - Then, based on the worker assistant you would like to call, which will be described in the JSON you
                generated, the system will execute the worker assistant call, and then provide "you" the output of the
                assistant in a new message with the role 'assistant'.
                - Then, it is up to you to decide if the response of the worker assistant tool is enough for you to
                 respond to the user with the natural language (or however requested from the user), or if you would
                 like to use another worker assistant tool, or same worker assistant again with different query, etc.

            3. You ''''''CANNOT'''''' share multiple JSON files in a single response, as the system NEEDS TO execute
            them one by one, and provide you the output of the tools. MAKE SURE that the JSON file you share is in the
            correct format, to prevent any errors. REMEMBER; if you put MULTIPLE JSON FILES; your execution WILL
            FAIL. Therefore, you can only share a single JSON file in a single response; make sure you stick to this
            rule.

        - A standardized format for the JSON file that you will output is as follows:

        '''
        {{
            "tool": "{{ToolTypeNames.ORCHESTRATION_WORKER_ASSISTANT_CALL}}",
            "parameters": {{
                "assistant_id": 0,  # The ID of the worker assistant you would like to call, NOT THE NAME OF THE ASSISTANT. DO NOT PUT COMMENTS IN THE JSON CALLS.
                "query": "The message you would like to send to the worker assistant",
                "file_urls": ["https://url-to-your-file-here", "https://url-to-your-file-here"],  # The URLs of the files you would like to share with the worker assistant.
                "image_urls": ["https://url-to-your-image-here", "https://url-to-your-image-here"]  # The URLs of the images you would like to share with the worker assistant.
            }}
        }}
        '''

        **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.
        **YOU MUST ALWAYS: ** share full URLs for the files and images you would like to share with the worker
        assistant. NEVER use relative URLs, as the system will not be able to reach them.

        - The "tool" parameter will be the name of the tool you would like to use, and the "parameters" will be the
        parameters for you to provide to the tool to execute.

        - The "assistant_id" parameter will be the ID of the worker assistant you would like to call, and the "query"
        will be the message you would like to send to the worker assistant. The "file_urls" and "image_urls" will be
        the URLs of the files and images you would like to share with the worker assistant. If you don't have any
        files or images to share, you can simply leave the lists empty, however, to prevent any unexpected errors,
        still provide the lists in the JSON file although with an empty list denotation '[]'.

        - **BE AWARE:** YOU MUST STRICTLY FOLLOW THE DICTIONARY FORMAT PROVIDED ABOVE. NEVER, EVER, CHANGE THE FORMAT
        OF THE DICTIONARY YOU OUTPUT. Start with ''', then open the curly braces, then write your JSON, then close the
        curly braces, and then close with '''. DO NOT EVER write 'json' next to the "'''" elements or anything else.

        - For every tool you have, a sample JSON file will be provided for you to understand how the tool will
        be called.

        - **NOTE about ORCHESTRATION LIMITS:** There are system limits implemented in the background, limiting
        the number of assistants that can be reached out in a single 'orchestration pipeline'. Orchestration pipeline
        means that you reach out a worker assistant, and then receive a message from it; and then you call a 'distinct'
        worker assistant again. Calling the same assistant multiple times '''IS NOT''' counted towards this limit.

        - If you hit this limit, the system will append an error message to the conversation, and this is how you will
        be aware of the issue. If you see this message, you should consider changing your strategy, and trying again.
        THEREFORE, the limits are in place for ''a single orchestration pipeline'', and NOT for the whole
        conversation you have within the query/response cycle.

        **THE LIMITS:**

        - The maximum number of 'different' distinct worker assistants that can be used in a single
        ''orchestration pipeline'':
    """

    response_prompt += f"""
        - The maximum number of distinct worker assistants that can be called '''consecutively''' in a single
        ''orchestration pipeline'':

        {maestro.maximum_assistant_limits}

        ---
    """

    return response_prompt


def build_orchestration_workers_multi_modality_prompt(maestro):
    maestro: Maestro
    response_prompt = f"""
        **WORKER ASSISTANT MULTI-MODALITY USAGE ABILITY:** (Very important! - Make sure to UNDERSTAND this part well)

        - As an orchestration assistant, you are able to use worker assistants to provide better and more accurate
        responses to the user's questions when you believe that there would be a benefit in doing so. In this section
        of your prompt, you will receive the list of worker assistants that you have access to, their IDs, as well
        as the data sources & capabilities they have access to. This information will help you to understand which
        worker assistant can be the most helpful for you in the current context. Be careful in reaching out the right
        worker assistant, as the data sources and capabilities of the worker assistants are different from each other.

    ---
    """

    worker_assistants = maestro.workers.all()
    for i, worker in enumerate(worker_assistants):
        worker: Assistant
        response_prompt += f"""
            [Worker Assistant ID: {worker.id}]  # ALWAYS USE IDs WHILE CALLING THE WORKER ASSISTANTS, NEVER USE NAMES!
                [Worker Assistant Name: {worker.name}]  # NEVER USE names WHILE CALLING THE WORKER ASSISTANTS, USE 'ID', ALWAYS!
                [Worker Assistant Description: {worker.description}]
                [Worker Assistant Response Language: {worker.response_language}]
                [Worker Assistant Time Awareness: {worker.time_awareness}]
                [Worker Assistant Place Awareness: {worker.place_awareness}]
                [Worker Assistant Image Generation & Manipulation Capability: {worker.image_generation_capability}]

        """

        response_prompt += f"""
                [[Worker Assistant Data Sources & Capabilities]]
        """

        response_prompt += f"""
                    [[[Worker Assistant SQL Database Connections]]]
        """

        for sql_source in worker.sql_database_connections.all():
            sql_source: SQLDatabaseConnection

            response_prompt += f"""
                        [[[[SQL Data Source ID: {sql_source.id}]]]]
                            [[[[[DBMS System Type: {sql_source.dbms_type}]]]]]
                            [[[[[Database Name: {sql_source.database_name}]]]]]
                            [[[[[Database Description: {sql_source.description}]]]]]
                            [[[[[Read Permissions: YES]]]]]
                            [[[[[Write Permissions: {not sql_source.is_read_only}]]]]]
                            [[[[[Maximum Records to Retrieve per Query (LIMIT): {sql_source.one_time_sql_retrieval_instance_limit}]]]]]

                            [[[[[Custom Queries of this Datasource:]]]]]
                            -------
            """

            for custom_query in sql_source.custom_queries.all():
                custom_query: CustomSQLQuery
                response_prompt += f"""
                                [[[[[[Custom Query ID: {custom_query.id}]]]]]]
                                    [[[[[[[[Query Data Source ID: {custom_query.database_connection.id}]]]]]]]]
                                    [[[[[[[[Query Name: {custom_query.name}]]]]]]]]
                                    [[[[[[[[Query Description: {custom_query.description}]]]]]]]]
                """

        response_prompt += f"""
                    [[[Worker Assistant Media Storage Connections]]]
        """

        for media_source in worker.datasourcemediastorageconnection_set.all():
            media_source: DataSourceMediaStorageConnection
            response_prompt += f"""
                        [[[[Media Storage Data Source ID: {media_source.id}]]]]
                            [[[[[Media Storage Name: {media_source.name}]]]]]
                            [[[[[Media Storage Description: {media_source.description}]]]]]
                            [[[[[Media Category: {media_source.media_category}]]]]]

                            *Names and Descriptions of the Media Items:*
                        """

            for media_item in media_source.items.all():
                media_item: DataSourceMediaStorageItem
                response_prompt += f"""
                                [[[[[[Media Item ID: {media_item.id}]]]]]]
                                    [[[[[[[File Name: {media_item.media_file_name}]]]]]]]
                                    [[[[[[[Description: {media_item.description}]]]]]]]
                                    [[[[[[[Media File Type: {media_item.media_file_type}]]]]]]]
                                    [[[[[[[Created At: {media_item.created_at}]]]]]]]
                """

        response_prompt += f"""
                    [[[Worker Assistant Knowledge Base Connections]]]
        """

        for kb in worker.documentknowledgebaseconnection_set.all():
            kb: DocumentKnowledgeBaseConnection
            response_prompt += f"""
                        [[[[Knowledge Base Data Source ID: {kb.id}]]]]
                            [[[[[System Provider: {kb.provider}]]]]]
                            [[[[[Knowledge Base Name: {kb.name}]]]]]
                            [[[[[Knowledge Base Class Name: {kb.class_name}]]]]]
                            [[[[[Knowledge Base Description: {kb.description}]]]]]]
                            [[[[[Number of Documents in the Knowledge Base: {kb.knowledge_base_documents.count()}]]]]]
                            [[[[[Maximum Records to Retrieve per Query (LIMIT): {kb.search_instance_retrieval_limit}]]]]]

                            """

        response_prompt += f"""
                    [[[Worker Assistant File System (SSH) Connections]]]
        """

        for fs_source in worker.data_source_file_systems.all():
            fs_source: DataSourceFileSystem
            response_prompt += f"""
                        [[[[File System Data Source ID: {fs_source.id}]]]]
                            [[[[[Operating System Type: {fs_source.os_type}]]]]]
                            [[[[[File System Name: {fs_source.name}]]]]]
                            [[[[[File System Description: {fs_source.description}]]]]]
                            [[[[[Host URL: {fs_source.host_url}]]]]]
                            [[[[[Port: {fs_source.port}]]]]]
                            [[[[[Username: {fs_source.username}]]]]]
                            [[[[[Maximum Records to Retrieve per Query (LIMIT): {fs_source.os_read_limit_tokens}]]]]]
                            [[[[[Is Read Only: {fs_source.is_read_only}]]]]]
                            """

        response_prompt += f"""
                    [[[Worker Assistant Machine Learning Model Connections]]]
        """

        for ml_source in worker.datasourcemlmodelconnection_set.all():
            ml_source: DataSourceMLModelConnection
            response_prompt += f"""
                        [[[[ML Model Data Source ID: {ml_source.id}]]]]
                            [[[[[ML Model Name: {ml_source.name}]]]]]
                            [[[[[ML Model Description: {ml_source.description}]]]]]
                            [[[[[Ml Model Object Category: {ml_source.model_object_category}]]]]]

                                *Names and Descriptions of the ML Models within this Connection:*
                            """

            ml_model_items = ml_source.items.all()
            for j, model_item in enumerate(ml_model_items):
                model_item: DataSourceMLModelItem
                response_prompt += f"""
                                [[[[[[ML Model Item ID: {model_item.id}]]]]]]
                                    [[[[[[[ML Model Name: {model_item.ml_model_name}]]]]]]]
                                    [[[[[[[ML Model Description: {model_item.description}]]]]]]]
                            """

        response_prompt += f"""
                    [[[Worker Assistant Browser Connections]]]
        """

        for browser_source in worker.datasourcebrowserconnection_set.all():
            browser_source: DataSourceBrowserConnection
            response_prompt += f"""
                        [[[[Browsing Datasource ID: {browser_source.id}]]]]
                            [[[[[Browser Type: {browser_source.browser_type}]]]]]
                            [[[[[Name: {browser_source.name}]]]]]
                            [[[[[Description: {browser_source.description}]]]]]
                            [[[[[Data Selectivity: {browser_source.data_selectivity}]]]]]
                            [[[[[Minimum Investigation Sites: {browser_source.minimum_investigation_sites}]]]]]
                            [[[[[Whitelisted Extensions: {browser_source.whitelisted_extensions}]]]]]
                            [[[[[Blacklisted Extensions: {browser_source.blacklisted_extensions}]]]]]
                            [[[[[Reading Abilities: {browser_source.reading_abilities}]]]]]
                            """

        response_prompt += f"""
                [[[Worker Assistant Tool Capabilities]]]
        """

        response_prompt += f"""
                    ** General Capabilities: **
                    [[[Worker Assistant Audio Processing Tool]]]
                    [[[Worker Assistant Code Interpreter & File Analysis Tool]]]
                    [[[Worker Assistant File System Command Execution Tool]]]  # Note: only if there is a file system connection
                    [[[Worker Assistant Image Generation Tool]]]  # Note: only if there is an image generation capability
                    [[[Worker Assistant Image Interpretation Tool]]]
                    [[[Worker Assistant Code Execution Tool]]]
                    [[[Worker Assistant Script Execution Tool]]]  # Note: only if there is a file system connection
                    [[[Worker Assistant Image Modification Tool]]]
                    [[[Worker Assistant Image Variation Tool]]]
                    [[[Worker Assistant Knowledge Base Search Query Execution Tool]]]  # Note: only if there is a knowledge base connection
                    [[[Worker Assistant Machine Learning Model Prediction Tool]]]  # Note: only if there is a machine learning model connection
                    [[[Worker Assistant SQL Query Execution Tool]]]  # Note: only if there is a SQL database connection
                    [[[Worker Assistant Storage Query Execution Tool]]]  # Note: only if there is a media storage connection
        """

        response_prompt += f"""
                    [[[Worker Assistant Custom Function Capabilities]]]
        """

        for function_reference in worker.customfunctionreference_set.all():
            function_reference: CustomFunctionReference
            custom_function: CustomFunction = function_reference.custom_function
            response_prompt += f"""
                        [[[[Custom Function Reference ID: {function_reference.id}]]]]
                            [[[[[Custom Function Name: {custom_function.name}]]]]]
                            [[[[[Custom Function Description: {custom_function.description}]]]]]
                            [[[[[Input Fields: {custom_function.input_fields}]]]]]
                            [[[[[Output Fields: {custom_function.output_fields}]]]]]
                            """

        response_prompt += f"""
                    [[[Worker Assistant Custom API Capabilities]]]
        """

        for api_reference in worker.customapireference_set.all():
            api_reference: CustomAPIReference
            custom_api: CustomAPI = api_reference.custom_api
            response_prompt += f"""
                        [[[[Custom API Reference ID: {api_reference.id}]]]]
                            [[[[[Custom API Name: {custom_api.name}]]]]]
                            [[[[[Custom API Description: {custom_api.description}]]]]]
                            [[[[[API Base URL: {custom_api.base_url}]]]]]
                            """

        response_prompt += f"""
                    [[[Worker Assistant Custom Script Capabilities]]]
        """

        for script_reference in worker.customscriptreference_set.all():
            script_reference: CustomScriptReference
            custom_script: CustomScript = script_reference.custom_script
            response_prompt += f"""
                        [[[[Custom Script Reference ID: {script_reference.id}]]]]
                            [[[[[Custom Script Name: {custom_script.name}]]]]]
                            [[[[[Custom Script Description: {custom_script.description}]]]]]
                           """

    response_prompt += """
    ---

    '''

    **NOTE**: These are the SQL Database Connections that you have access to. Make sure to keep these in mind
    while responding to the user's messages. Custom queries are also provided for each SQL Database Connection,
    which you can use to fetch data from the respective database or if you have the write permissions, you
    can use them to write data to the respective database. If this part is EMPTY, it means that the user has
    not provided any SQL Database Connections, so neglect this part if that is the case.

    **NOTE about DBMS Schema:** The DBMS Schema is provided for your reference to help you understand what
    kind of data types and tables are available in the respective database.

    **NOTE about RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
    the 'Maximum Records to Retrieve per Query (LIMIT)' field. Please make sure to follow these limits when
    executing the SQL queries by always embedding the 'LIMIT' clause in your SQL queries, even if they are
    not present in a custom query. This is very important to ensure that the system does not overload the
    database with a large number of records.
    """

    return response_prompt


def build_structured_tool_prompt__orchestration_worker_assistant_call_execution():
    response_prompt = f"""
        **TOOL**: Worker Assistant Calling Tool

        - The Worker Assistant Calling Tool is a tool that allows you to call worker assistants to provide better and
        more accurate responses to the user's questions when you believe that there would be a benefit in doing so.
        The Worker Assistant Calling Tool is a dedicated tool for calling worker assistants to execute a query on a
        certain request / requirement of the user; and also lets you to send image URLs, or file URLs depending on the
        requirements specified to you by the user's query. Don't forget that you can only share a single JSON file in
        a single request, and make sure you stick to this rule.

        - The standardized format for the dictionary that you will output to use the Worker Assistant Calling Tool
        is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_ORCHESTRATION_WORKER_CONSULTANCY}",
                "parameters": {{
                    "assistant_id": 0,  # The ID of the worker assistant you would like to call, NEVER THE NAME OF THE ASSISTANT, USE THE ID!
                    "query": "The message you would like to send to the worker assistant",
                    "file_urls": ["https://url-to-your-file-here", "https://url-to-your-file-here"],  # The URLs of the files you would like to share with the worker assistant.
                    "image_urls": ["https://url-to-your-image-here", "https://url-to-your-image-here"]  # The URLs of the images you would like to share with the worker assistant.
                }}
            }}
        '''

        **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        **INSTRUCTIONS:** The "assistant_id" field should be the ID of the worker assistant you would like to call.
        The "query" field should be the message you would like to send to the worker assistant. The "file_urls" and
        "image_urls" fields should be lists of strings that contain the URLs of the files and images that you would
        like to share with the worker assistant. If you don't have any files or images to share, you can simply leave
        the lists empty, however, to prevent any unexpected errors, still provide the lists in the JSON file although
        with an empty list denotation '[]'.

        To use this tool, you need to provide the following field 'VERY CAREFULLY':

        1. For "assistant_id", provide the ID of the worker assistant you would like to call. You can find the ID of
        the worker assistant you would like to call in the relevant section of your prompt where the worker assistants
        you have access to are listed and their IDs are provided. In that section, every information and detail you
        require for selecting a relevant worker assistant tool are provided with you; so that you can understand what
        assistant can be the most helpful for you in the current context.

        2. For "query", provide the message you would like to send to the worker assistant. This message should be
        in natural language, and should be a clear and concise message that describes the query you would like to
        execute on the worker assistant. This message will be directly sent to the worker assistant; similar to a
        user message sent to an AI assistant in a conversation; only that this time, you are the one sending the
        message to the worker assistant; and that assistant now has to reply you. DO NOT expect the user to reach out
        to the assistant themselves; because they can't. You are the sole orchestrator and the only subject
        responsible for using the worker assistants to help the user; so in cases where the assistants fails to deliver
        certain necessities, you are the one who should take the responsibility to optimize your conversation with the
        assistant and make them respond to the user's query in the best way possible. The assistants are also able
        to remember your conversations with them, so you can mention previous messages you sent to them in your
        conversation; however, don't assume different assistants to be aware of the previous messages you sent to
        another assistant; because they are not aware of the messages you sent to other assistants; they are only
        aware of the messages you sent to them (your assistant conversations are 1 to 1, and not shared among the
        assistants).

        3. For "file_urls" and "image_urls", provide the URLs of the files and images that you would like to share
        with the worker assistant. You can provide the URLs of the files and images that you would like to share with
        the worker assistant. If you don't have any files or images to share, you can simply leave the lists empty,
        however, to prevent any unexpected errors, still provide the lists in the JSON file although with an empty list
        denotation '[]'.

        ---

        **IMPORTANT NOTES:**

        - The responses you receive from the assistants can have multiple different sections:
            i. Textual part: The textual part of the response, which is the main response of the assistant to your
                query.
            ii. File URIs: The URIs of the files that are generated as a result of the query. You can use these URIs
                to provide the user with the files that are generated as a result of the query, if that is necessary,
                or if you have got URLs from the assistants at all.
            iii. Image URIs: The URIs of the images that are generated as a result of the query. You can use these URIs
                to provide the user with the images that are generated as a result of the query, if that is necessary,
                or if you have got URLs from the assistants at all.

        **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
        have the output of the execution, and you will be expected to take this response and EITHER provide an answer
        to the user's question based on the response that you receive, in your own words; OR decide to utilize an
        additional worker assistant tool to proceed with the next steps. Think of the worker assistant tools as
        as employees of yours that you are instructing to execute a query on something, and you are expected
        to take the response of this employee and provide an answer to the user's question based on the response
        that you receive from this employee.

        **ABOUT YOU PROVIDING LINKS:**
        - If you need to provide a direct link to the user for reaching the files, here is the base
            URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
            - {MEDIA_URL}
        - **NEVER, EVER:** provide a 'relative' path to the files. Always provide the 'absolute' path by
        appending the file path to the base URL.

    """
    return response_prompt
