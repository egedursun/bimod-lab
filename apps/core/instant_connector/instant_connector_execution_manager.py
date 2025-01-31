#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: instant_connector_execution_manager.py
#  Last Modified: 2025-01-28 14:24:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-28 14:24:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from apps.core.instant_connector.utils import (
    InstantConnectionTypes
)
from apps.core.nosql.nosql_executor import (
    CouchbaseNoSQLExecutor,
    ElasticSearchNoSQLExecutor,
    MongoDBNoSQLExecutor,
    Neo4JNoSQLExecutor,
    RedisNoSQLExecutor,
    WeaviateNoSQLExecutor
)

from apps.core.sql.sql_executor import (
    MariaDBExecutor,
    MSSQLExecutor,
    MySQLExecutor,
    OracleDBExecutor,
    PostgresSQLExecutor
)

logger = logging.getLogger(__name__)


class InstantConnectionExecutionManager:

    def __init__(self, connection_string):
        self.connection_params = {
            "type": None,
            "subtype": None,
            "username": None,
            "password": None,
            "host": None,
            "port": None,
            "database_name": None,
        }

        """
        Sample Connection String:
        sql.postgresql://username:password@host:port/database_name
        nosql.mongodb://username:password@host:port/database_name
        """

        success, message = self._pre_validate_connection_string(
            connection_string=connection_string
        )

        if not success:
            logger.error(message)

        self.connection_params = self._parse_connection_string(
            connection_string=connection_string
        )

        success, message = self._validate_connection_params(
            connection_params=self.connection_params
        )

        if not success:
            logger.error(message)

    @staticmethod
    def _pre_validate_connection_string(
        connection_string: str
    ):
        if not connection_string:
            error_message = "Connection string is empty. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if "://" not in connection_string:
            error_message = "Connection string is invalid. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if connection_string.count("://") != 1:
            error_message = "Connection string is invalid. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if connection_string.count("@") != 1:
            error_message = "Connection string is invalid. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        return True, None

    @staticmethod
    def _parse_connection_string(
        connection_string: str
    ):
        connection_params = {
            "type": None,
            "subtype": None,
            "username": None,
            "password": None,
            "host": None,
            "port": None,
            "database_name": None,
        }

        types_part = connection_string.split("://")[0]
        type_ = types_part.split(".")[0]
        subtype = types_part.split(".")[1]
        connection_params["type"] = type_
        connection_params["subtype"] = subtype

        credentials_part = connection_string.split("://")[1].split("@")[0]
        username = credentials_part.split(":")[0]
        password = credentials_part.split(":")[1]
        connection_params["username"] = username
        connection_params["password"] = password

        host_port_part = connection_string.split("://")[1].split("@")[1].split("/")[0]
        host = host_port_part.split(":")[0]
        port = host_port_part.split(":")[1]
        connection_params["host"] = host
        connection_params["port"] = port

        if type != InstantConnectionTypes.SERVER:
            database_bucket = connection_string.split("://")[1].split("@")[1].split("/")[1]
            connection_params["database_name"] = database_bucket

        else:
            pass

        return connection_params

    @staticmethod
    def _validate_connection_params(
        connection_params: dict
    ):
        if not connection_params["type"]:
            error_message = "Connection type is missing. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if connection_params["type"] not in [
            InstantConnectionTypes.SQL,
            InstantConnectionTypes.NOSQL,
            InstantConnectionTypes.SERVER
        ]:
            error_message = "Connection type is invalid. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if not connection_params["subtype"]:
            error_message = "Connection subtype is missing. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if connection_params["type"] == InstantConnectionTypes.SQL:
            if connection_params["subtype"] not in InstantConnectionTypes.get_sql_valid_subtypes():
                error_message = "Connection subtype for SQL is invalid. Please provide a valid connection string."
                logger.error(error_message)
                return False, error_message

        if connection_params["type"] == InstantConnectionTypes.NOSQL:
            if connection_params["subtype"] not in InstantConnectionTypes.get_nosql_valid_subtypes():
                error_message = "Connection subtype for NoSQL is invalid. Please provide a valid connection string."
                logger.error(error_message)
                return False, error_message

        if connection_params["type"] == InstantConnectionTypes.SERVER:
            if connection_params["subtype"] not in InstantConnectionTypes.get_server_valid_subtypes():
                error_message = "Connection subtype for Server is invalid. Please provide a valid connection string."
                logger.error(error_message)
                return False, error_message

        if not connection_params["username"]:
            error_message = "Connection username is missing. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if not connection_params["password"]:
            error_message = "Connection password is missing. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if not connection_params["host"]:
            error_message = "Connection host is missing. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if not connection_params["port"]:
            error_message = "Connection port is missing. Please provide a valid connection string."
            logger.error(error_message)
            return False, error_message

        if connection_params["type"] != InstantConnectionTypes.SERVER:
            if not connection_params["database_name"]:
                error_message = "Connection database bucket is missing. Please provide a valid connection string."
                logger.error(error_message)
                return False, error_message

        return True, None

    def execute_query_or_command(self, assistant, query_command):

        if self.connection_params["type"] == InstantConnectionTypes.SQL:

            if self.connection_params["subtype"] == "postgresql":
                output = PostgresSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "mysql":
                output = MySQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "mssql":
                output = MSSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "mariadb":
                output = MariaDBExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "oracle":
                output = OracleDBExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            else:
                logger.error("Connection subtype is invalid. Please provide a valid connection string.")
                return "Connection subtype is invalid. Please provide a valid connection string."

        elif self.connection_params["type"] == InstantConnectionTypes.NOSQL:
            if self.connection_params["subtype"] == "mongodb":
                output = MongoDBNoSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "couchbase":
                output = CouchbaseNoSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "elasticsearch":
                output = ElasticSearchNoSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "neo4j":
                output = Neo4JNoSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "weaviate":
                output = WeaviateNoSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            elif self.connection_params["subtype"] == "redis":
                output = RedisNoSQLExecutor.execute_read__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    query=query_command,
                    parameters=None
                )

            else:
                logger.error("Connection subtype is invalid. Please provide a valid connection string.")
                return "Connection subtype is invalid. Please provide a valid connection string."

        elif self.connection_params["type"] == InstantConnectionTypes.SERVER:

            from apps.core.file_systems.file_systems_executor import (
                FileSystemsExecutor
            )

            if self.connection_params["subtype"] == "ssh":

                output_list = FileSystemsExecutor.execute_file_system_command_set__headless(
                    assistant=assistant,
                    connection_params=self.connection_params,
                    commands=[
                        query_command
                    ],
                )

                # Unlike the other methods, the result of this function is a list, convert it to string
                output = str(output_list)

            else:
                logger.error("Connection subtype is invalid. Please provide a valid connection string.")
                return "Connection subtype is invalid. Please provide a valid connection string."

        else:
            error_message = "Connection type is invalid. Please provide a valid connection string."
            logger.error(error_message)
            return error_message

        return output
