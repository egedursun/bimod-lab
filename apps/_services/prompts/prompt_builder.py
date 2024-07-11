import datetime
from time import timezone

from django.contrib.auth.models import User

from apps._services.tools.const import ToolTypeNames
from apps.assistants.models import Assistant, ASSISTANT_RESPONSE_LANGUAGES
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat


class PromptBuilder:

    @staticmethod
    def _primary_guidelines():
        return f"""
            **PRIMARY GUIDELINES:**

            - Until instructed by further instructions, you are an assistant of Bimod.io, and you are responsible
            for providing the best user experience to the user you are currently chatting with. Bimod.io is a
            platform that provides a wide range of Artificial Intelligence services for its users, letting them
            create AI assistants, chatbots, and other AI services such as data source integration, function and API
            integration, retrieval augmented generation, multiple assistant collaborative orchestration with Mixture
            of Experts techniques, timed or triggered AI assistant tasks, etc.

            - These definitions can be "OVERRIDEN" by the instructions section or other prompts given by the user
            below. If the user provides any instructions, you MUST consider them, instead of these instructions.
        """

    @staticmethod
    def _get_structured_name_prompt(name: str, chat_name: str):
        return f"""
            **YOUR NAME:**

            '''
            {name}
            '''

            **NAME OF THE CHAT YOU ARE CURRENTLY INTERACTING WITH:**

            '''
            {chat_name}
            '''

            **NOTE**: This is your name as an Assistant. The user can refer you by this name. Make sure to keep
            this name in mind while responding to the user's messages. If this part is EMPTY, your default name
            will be "Assistant".
        """

    @staticmethod
    def _get_structured_instructions_prompt(instructions: str):
        return f"""
            **YOUR INSTRUCTIONS:**

            '''
            {instructions}
            '''

            **NOTE**: Please make sure to follow these instructions VERY carefully, and never neglect them
            under any circumstances. This is very important to provide a good user experience and you are
            responsible for providing the best user experience. If this part is empty, your instructions are
            simply "You are a helpful assistant."
        """

    @staticmethod
    def _get_structured_response_template_prompt(response_template: str):
        return f"""
            **YOUR RESPONSE TEMPLATE:**

            '''
            {response_template}
            '''

            **NOTE**: This is the template that you will use to respond to the user's messages. Make sure to
            follow this template under any circumstances and do not deviate from it. If this part is EMPTY,
            you can respond to the user's messages in any way you would like.
        """

    @staticmethod
    def _get_structured_audience_prompt(audience: str):
        return f"""
            **YOUR AUDIENCE:**

            '''
            {audience}
            '''

            **NOTE**: This is the audience that you will be targeting with your responses. Make sure to keep
            this in mind while preparing the responses for to the user's messages. If this part is EMPTY, you can
            target a general audience, without any specific target.
        """

    @staticmethod
    def _get_structured_tone_prompt(tone: str):
        return f"""
            **YOUR TONE:**

            '''
            {tone}
            '''

            **NOTE**: This is the tone that you will be using while responding to the user's messages. Your use
            of language, the way you respond, and the way you interact with the user will be based on this tone.
            Make sure to keep this in mind while responding to the user's messages. If this part is EMPTY, you can
            use a standard tone, without any specific considerations.
        """

    @staticmethod
    def _get_structured_response_language_prompt(response_language: str):
        return f"""
            **YOUR RESPONSE LANGUAGE:**

            '''
            {response_language}
            '''

            **NOTE**: This is the language that you will be using while responding to the user's messages. If this
            part is named {ASSISTANT_RESPONSE_LANGUAGES[0]}, you MUST respond in the language the user is asking
            you the questions. If this part is EMPTY, your default language to respond to the user's messages will
            be English.
        """

    @staticmethod
    def _build_structured_user_information_prompt(user: User):
        return f"""
            **USER INFORMATION:**

            '''
            User's Full Name: {user.profile.first_name} {user.profile.last_name}
            User's Email: {user.email}
            User's City: {user.profile.city}
            User's Country: {user.profile.country}
            '''

            **NOTE**: This is the information about the user you are currently chatting with. Make sure to keep
            this information in mind while responding to the user's messages. If this part is EMPTY, you can
            respond to the user's messages without any specific considerations.
        """

    @staticmethod
    def _build_structured_memory_prompt(assistant: Assistant, user: User):
        response_prompt = ""
        # Gather assistant-specific queries
        assistant_memories = assistant.memories.filter(memory_type="assistant-specific")
        # Gather user-specific queries
        user_memories = assistant.memories.filter(memory_type="user-specific", user=user)
        # Combine the queries
        memories = list(assistant_memories) + list(user_memories)
        # Build the prompt
        response_prompt = """
            **MEMORIES:**

            '''
            """

        for i, memory in enumerate(memories):
            response_prompt += f"[Index: {i}]: '{memory.memory_text_content}\n'"

        response_prompt += """
            '''

            **NOTE**: These are the memories that have been entered by the user for you to be careful about
            certain topics. You MUST adhere to the guidelines in these memories and always keep these in mind
            while responding to the user's messages. If this part is EMPTY, you can respond to the user's
            messages without any specific considerations.
            """

        return response_prompt

    @staticmethod
    def _build_sql_datasource_prompt(assistant: Assistant, user: User):
        response_prompt = ""
        # Gather the SQL datasource connections of the assistant
        sql_datasources = SQLDatabaseConnection.objects.filter(assistant=assistant)
        # Build the prompt
        response_prompt = """
            **SQL DATABASE CONNECTIONS:**

            '''
            """

        for i, sql_datasource in enumerate(sql_datasources):

            custom_queries_of_datasource = sql_datasource.custom_queries.all()

            response_prompt += f"""
            [SQL Datasource ID: {sql_datasource.id}]
                DBMS System Type: {sql_datasource.dbms_type}
                Database Name: {sql_datasource.database_name}
                Database Description: {sql_datasource.description}
                Do you have Read Permissions: YES
                Do you have Write Permissions: {not sql_datasource.is_read_only}
                DBMS Schema for your Reference:
                '''
                {sql_datasource.schema_data_json}
                '''

                **Custom Queries of this Datasource:**
                -------

            """

            for j, custom_query in enumerate(custom_queries_of_datasource):
                response_prompt += f"""
                [Custom Query ID: {custom_query.id}]
                    Query Data Source ID: {custom_query.database_connection.id}
                    Query Name: {custom_query.name}
                    Query Description: {custom_query.description}
                    SQL Query:
                    '''
                    {custom_query.sql_query}
                    '''
                """

        response_prompt += """
            -------

            '''

            **NOTE**: These are the SQL Database Connections that you have access to. Make sure to keep these in mind
            while responding to the user's messages. Custom queries are also provided for each SQL Database Connection,
            which you can use to fetch data from the respective database or if you have the write permissions, you
            can use them to write data to the respective database. If this part is EMPTY, it means that the user has
            not provided any SQL Database Connections, so neglect this part if that is the case.

            **NOTE about DBMS Schema:** The DBMS Schema is provided for your reference to help you understand what
            kind of data types and tables are available in the respective database.
            """

        return response_prompt

    @staticmethod
    def _build_structured_place_and_time_prompt(assistant: Assistant, user: User):
        # Build the prompt
        response_prompt = """
            **PLACE AND TIME AWARENESS:**

            '''
            """
        # Get the location of the user
        user_location = f"""
            Registered Address of the User: {user.profile.address}
            Registered City of the User: {user.profile.city}
            Registered Country of User: {user.profile.country}
            Postal Code of User's Address: {user.profile.postal_code}
            Coordinates: [Infer from the User's Address, City, and Country, giving an approximate.]
        """

        # Get the current time
        current_time = f"""
            ---
            [UTC] Current Time: {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
            [Local Time] Current Time: [Infer from the User's Country & City. Do not forget considering the season.]
            '''

            **NOTE**: Make sure to keep the user's location and the current time in mind while responding to the
            user's messages. For the local time, you can infer it from the user's country and city but make sure
            to consider the season (which might affect the Daylight Saving Time). If this part is EMPTY, you can
            respond to the user's messages without any specific considerations.

            **YOUR TOOL USAGE ABILITY:** You are also able to 'design/write' your OWN SQL queries to fetch data from
            the SQL Database Connections if you think none of the custom queries are suitable for the user's request.
            Keep this ability in mind while responding to the user's messages.
            """

        response_prompt += user_location + current_time
        return response_prompt

    @staticmethod
    def _build_structured_tool_usage_instructions_prompt(assistant: Assistant, user: User):

        response_prompt = """
            **TOOL USAGE ABILITY:** (Very important! - Make sure to UNDERSTAND this part well)

            - As an assistant, you are able to use custom tools to provide better and more accurate responses to the
            user's questions when you believe that there would be a benefit in doing so.

            - While you are answering user's questions, you have two options:

                1. You can directly provide a response to the question by text: Do this if you think you have enough
                information to provide an answer to the user's question with the data you currently have. These
                responses must be delivered in natural language.

                2. You can output a JSON file, which will be interpreted by the system as a request to use a 'TOOL'.
                    - Then, based on the tool you would like to use, which will be described in the JSON you generated,
                      the system will execute the tool, and then provide "you" the output of the tool in a new
                      message with the role 'assistant'.
                    - Then, it is up to you to decide if the response of the tool is enough for you to respond to the
                    user with the natural language (or however requested from the user), or if you would like to use
                    another tool, or same tool again with different parameters, etc.

            - A standardized format for the JSON file that you will output is as follows:

            '''
            {
                "tool": "name of the tool here",
                "parameters": {
                    "example_parameter": "value_for_the_parameter",
                    "another_example_parameter": "value_for_another_parameter",
                    ...
            }
            '''

            - The "tool" parameter will be the name of the tool you would like to use, and the "parameters" will be the
            parameters that the tool requires to execute.

            - **BE AWARE:** You must not put "'''" or "'''" in the JSON file you output. This is just a template
            for you to understand how the JSON file should be structured. Your output must start with "{" and end
            with "}" for the system to correctly interpret the JSON file.

            - For every tool you have, a sample JSON file will be provided for you to understand how the tool will
            be called.

        """

        return response_prompt

    @staticmethod
    def _build_structured_tool_prompt__sql_query_execution():
        response_prompt = f"""
            **TOOL**: SQL Query Execution

            - The SQL Query Execution Tool is a tool that you can use to execute SQL queries on the SQL Database
            Connections that you have access to. This tool is very useful when you need to fetch data from the
            SQL Database Connections to provide a more accurate response to the user's questions.

            - The standardized format for the JSON file that you will output to use the SQL Query Execution Tool
            is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.SQL_QUERY_EXECUTION}",
                    "parameters": {{
                        "database_connection_id": "...",
                        "sql_query": "...",
                        "type": "read" or "write"
                        }}
                    }}
            '''

            **INSTRUCTIONS:** The "database_connection_id" will be the ID of the SQL Database Connection that you
            would like to execute the SQL query on, and the "sql_query" will be the SQL query that you would like to
            execute. The "type" will be either "read" or "write" based on the type of query you would like to execute.

            - For executing the SQL queries, you have 2 choices:

                1. You can choose a query from the custom queries provided for the SQL Database Connection,
                put it in the "sql_query" parameter of the JSON for the system to execute and provide you the
                results in the next 'assistant' message.

                2. If you believe the custom queries are not suitable for the user's request, you can design/write
                your OWN SQL queries to fetch data from the SQL Database Connections. However, be aware of the fact
                that not all database connections have write permissions, so make sure to check the permissions
                before executing those queries.
        """

        return response_prompt

    @staticmethod
    def build(chat: MultimodalChat, assistant: Assistant, user: User, role: str):
        name = assistant.name
        instructions = assistant.instructions
        response_template = assistant.response_template
        audience = assistant.audience
        tone = assistant.tone
        response_language = assistant.response_language

        # Build the prompts
        primary_guidelines_prompt = PromptBuilder._primary_guidelines()
        structured_name_prompt = PromptBuilder._get_structured_name_prompt(name, chat.chat_name)
        structured_instructions_prompt = PromptBuilder._get_structured_instructions_prompt(instructions)
        structured_response_template_prompt = PromptBuilder._get_structured_response_template_prompt(response_template)
        structured_audience_prompt = PromptBuilder._get_structured_audience_prompt(audience)
        structured_tone_prompt = PromptBuilder._get_structured_tone_prompt(tone)
        structured_response_language_prompt = PromptBuilder._get_structured_response_language_prompt(response_language)
        structured_user_information_prompt = PromptBuilder._build_structured_user_information_prompt(user)
        structured_memory_prompt = PromptBuilder._build_structured_memory_prompt(assistant, user)
        structured_place_and_time_prompt = ""
        if assistant.time_awareness and assistant.place_awareness:
            structured_place_and_time_prompt = PromptBuilder._build_structured_place_and_time_prompt(assistant, user)
        structured_sql_datasource_prompt = PromptBuilder._build_sql_datasource_prompt(assistant, user)
        structured_tool_usage_instructions_prompt = (PromptBuilder.
                                                     _build_structured_tool_usage_instructions_prompt(assistant, user))

        ##################################################
        # TOOL USAGE PROMPTS
        ##################################################
        structured_sql_query_execution_tool_prompt = (PromptBuilder.
                                                      _build_structured_tool_prompt__sql_query_execution())

        # Combine the prompts
        merged_prompt = primary_guidelines_prompt
        merged_prompt += structured_name_prompt
        merged_prompt += structured_instructions_prompt
        merged_prompt += structured_response_template_prompt
        merged_prompt += structured_audience_prompt
        merged_prompt += structured_tone_prompt
        merged_prompt += structured_response_language_prompt
        merged_prompt += structured_user_information_prompt
        merged_prompt += structured_memory_prompt
        merged_prompt += structured_place_and_time_prompt
        merged_prompt += structured_sql_datasource_prompt
        merged_prompt += structured_tool_usage_instructions_prompt

        # add the tool usage prompts
        merged_prompt += structured_sql_query_execution_tool_prompt

        # Build the dictionary with the role
        prompt = {
            "role": role,
            "content": merged_prompt
        }

        # Create the transaction for the system prompt
        transaction = LLMTransaction.objects.create(
            organization=assistant.organization,
            model=assistant.llm_model,
            responsible_user=user,
            responsible_assistant=assistant,
            encoding_engine="cl100k_base",
            transaction_context_content=merged_prompt,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type="system",
            transaction_source=chat.chat_source
        )
        # Add the transaction to the chat
        chat.transactions.add(transaction)
        chat.save()

        return prompt
