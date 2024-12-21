#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: beamguard_executor.py
#  Last Modified: 2024-12-02 01:24:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:24:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from django.utils import timezone

from apps.assistants.models import Assistant

from apps.beamguard.models import (
    BeamGuardArtifact
)

from apps.core.beamguard.utils import (
    MYSQL_GUARDED_KEYWORDS,
    POSTGRESQL_GUARDED_KEYWORDS,
    UNIX_FILE_SYSTEM_GUARDED_KEYWORDS,
    MSSQL_GUARDED_KEYWORDS,
    ORACLE_GUARDED_KEYWORDS,
    MARIADB_GUARDED_KEYWORDS,

    #####

    N1QL_GUARDED_KEYWORDS,
    REDIS_GUARDED_KEYWORDS,
    ELASTICSEARCH_GUARDED_KEYWORDS,
    NEO4J_GUARDED_KEYWORDS,
    WEAVIATE_GRAPHQL_GUARDED_KEYWORDS,
)

from apps.core.nosql.nosql_executor import (
    CouchbaseNoSQLExecutor,
    MongoDBNoSQLExecutor,
    RedisNoSQLExecutor,
    ElasticSearchNoSQLExecutor,
    Neo4JNoSQLExecutor,
    WeaviateNoSQLExecutor
)

from apps.core.sql.sql_executor import (
    MySQLExecutor,
    PostgresSQLExecutor,
    MSSQLExecutor,
    OracleDBExecutor,
    MariaDBExecutor
)

from apps.datasource_file_systems.utils import (
    DataSourceFileSystemsOsTypeNames
)

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection
)

from apps.datasource_nosql.utils import (
    NoSQLDatabaseChoicesNames
)

from apps.datasource_sql.models import (
    SQLDatabaseConnection
)

from apps.datasource_sql.utils import (
    DBMSChoicesNames
)

from apps.multimodal_chat.models import (
    MultimodalChat
)

logger = logging.getLogger(__name__)


class BeamGuardExecutionManager:
    def __init__(
        self,
        assistant: Assistant,
        chat: MultimodalChat
    ):
        self.assistant: Assistant = assistant
        self.chat: MultimodalChat = chat

    #####

    def _guard_mysql_modifications(
        self,
        connection: SQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in MYSQL_GUARDED_KEYWORDS:

            if keyword in raw_query.upper():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in MySQL query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "SQL",
                        "dbms_type": connection.dbms_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "port": connection.port,
                        "database_name": connection.database_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    },
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.SQL,
                sql_connection_object=connection,
                # nosql_connection_object=None,
                # file_system_connection_object=None
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_postgresql_modifications(
        self,
        connection: SQLDatabaseConnection,
        raw_query: str
    ):

        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in POSTGRESQL_GUARDED_KEYWORDS:

            if keyword in raw_query.upper():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in PostgreSQL query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "SQL",
                        "dbms_type": connection.dbms_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "port": connection.port,
                        "database_name": connection.database_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.SQL,
                sql_connection_object=connection,
                # nosql_connection_object=None,
                # file_system_connection_object=None
            )
            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_mssql_modifications(
        self,
        connection: SQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in MSSQL_GUARDED_KEYWORDS:
            if keyword in raw_query.upper():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in MSSQL query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "SQL",
                        "dbms_type": connection.dbms_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "port": connection.port,
                        "database_name": connection.database_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.SQL,
                sql_connection_object=connection,
                # nosql_connection_object=None,
                # file_system_connection_object=None
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_oracle_modifications(
        self,
        connection: SQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in ORACLE_GUARDED_KEYWORDS:
            if keyword in raw_query.upper():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in Oracle query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "SQL",
                        "dbms_type": connection.dbms_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "port": connection.port,
                        "database_name": connection.database_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.SQL,
                sql_connection_object=connection,
                # nosql_connection_object=None,
                # file_system_connection_object=None
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_mariadb_modifications(
        self,
        connection: SQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in MARIADB_GUARDED_KEYWORDS:
            if keyword in raw_query.upper():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in MariaDB query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "SQL",
                        "dbms_type": connection.dbms_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "port": connection.port,
                        "database_name": connection.database_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.SQL,
                sql_connection_object=connection,
                # nosql_connection_object=None,
                # file_system_connection_object=None
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def guard_sql_modifications(
        self,
        connection_id: int,
        raw_query: str
    ):
        connection = SQLDatabaseConnection.objects.get(
            id=connection_id
        )

        db_type = connection.dbms_type

        if db_type == DBMSChoicesNames.MYSQL:
            artifact = self._guard_mysql_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif db_type == DBMSChoicesNames.POSTGRESQL:
            artifact = self._guard_postgresql_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif db_type == DBMSChoicesNames.MSSQL:
            artifact = self._guard_mssql_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif db_type == DBMSChoicesNames.ORACLE:
            artifact = self._guard_oracle_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif db_type == DBMSChoicesNames.MARIADB:
            artifact = self._guard_mariadb_modifications(
                connection=connection,
                raw_query=raw_query
            )

        else:
            logger.error(f"Unsupported DBMS type: {db_type}")

            return None

        if artifact:
            return artifact

        else:
            return None

    def _guard_couchbase_modifications(
        self,
        connection: NoSQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in N1QL_GUARDED_KEYWORDS:

            if keyword in raw_query.upper():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in Couchbase N1QL query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "NoSQL",
                        "nosql_db_type": connection.nosql_db_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "bucket_name": connection.bucket_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.NOSQL,
                # sql_connection_object=None,
                nosql_connection_object=connection,
                # file_system_connection_object=None
            )
            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_mongodb_modifications(
        self,
        connection: NoSQLDatabaseConnection,
        raw_query: str,
        query_type: str = None
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        if query_type.lower() == "read":
            return None

        try:

            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "NoSQL",
                        "nosql_db_type": connection.nosql_db_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "bucket_name": connection.bucket_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": "Update Query for MongoDB database collection.",
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.NOSQL,
                # sql_connection_object=None,
                nosql_connection_object=connection,
                # file_system_connection_object=None
            )
            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_redis_modifications(
        self,
        connection: NoSQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in REDIS_GUARDED_KEYWORDS:
            if keyword in raw_query.upper():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in Redis command: {raw_query}")

        try:

            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "NoSQL",
                        "nosql_db_type": connection.nosql_db_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "bucket_name": connection.bucket_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.NOSQL,
                nosql_connection_object=connection,
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_elasticsearch_modifications(
        self,
        connection: NoSQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in ELASTICSEARCH_GUARDED_KEYWORDS:

            raw_query_string = json.dumps(raw_query)

            if keyword in raw_query_string.upper():
                unauthorized_keyword_found = True

                unauthorized_keywords_list.append(
                    keyword
                )

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in Elasticsearch query: {raw_query}")

        try:

            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "NoSQL",
                        "nosql_db_type": connection.nosql_db_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "bucket_name": connection.bucket_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.NOSQL,
                nosql_connection_object=connection
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def _guard_neo4j_modifications(
        self,
        connection: NoSQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in NEO4J_GUARDED_KEYWORDS:

            if keyword in raw_query.upper():
                unauthorized_keyword_found = True

                unauthorized_keywords_list.append(
                    keyword
                )

        if (
            not unauthorized_keyword_found and
            not unauthorized_keywords_list
        ):
            return None

        logger.warning(f"Unauthorized keyword found in Neo4j query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "NoSQL",
                        "nosql_db_type": connection.nosql_db_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "port": connection.port,
                        "database_name": connection.bucket_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.NOSQL,
                nosql_connection_object=connection,
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created for Neo4j query: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact for Neo4j: {e}")

            return None

    def _guard_weaviate_modifications(
        self,
        connection: NoSQLDatabaseConnection,
        raw_query: str
    ):
        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in WEAVIATE_GRAPHQL_GUARDED_KEYWORDS:

            if keyword.lower() in raw_query.lower():
                unauthorized_keyword_found = True

                unauthorized_keywords_list.append(
                    keyword
                )

        if (
            not unauthorized_keyword_found and
            not unauthorized_keywords_list
        ):
            return None

        logger.warning(f"Unauthorized keyword found in Weaviate GraphQL query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "NoSQL",
                        "nosql_db_type": connection.nosql_db_type,
                        "name": connection.name,
                        "description": connection.description,
                        "host": connection.host,
                        "bucket_name": connection.bucket_name,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.NOSQL,
                nosql_connection_object=connection,
            )

            artifact.save()

            logger.info(f"BeamGuard artifact created for Weaviate query: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact for Weaviate: {e}")

            return None

    def guard_nosql_modifications(
        self,
        connection_id: int,
        raw_query: str,
        query_type: str = None
    ):
        connection = NoSQLDatabaseConnection.objects.get(
            id=connection_id
        )

        nosql_db_type = connection.nosql_db_type

        if nosql_db_type == NoSQLDatabaseChoicesNames.COUCHBASE:

            artifact = self._guard_couchbase_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif nosql_db_type == NoSQLDatabaseChoicesNames.MONGODB:

            artifact = self._guard_mongodb_modifications(
                connection=connection,
                raw_query=raw_query,
                query_type=query_type
            )

        elif nosql_db_type == NoSQLDatabaseChoicesNames.REDIS:

            artifact = self._guard_redis_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif nosql_db_type == NoSQLDatabaseChoicesNames.ELASTICSEARCH:

            artifact = self._guard_elasticsearch_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif nosql_db_type == NoSQLDatabaseChoicesNames.NEO4J:

            artifact = self._guard_neo4j_modifications(
                connection=connection,
                raw_query=raw_query
            )

        elif nosql_db_type == NoSQLDatabaseChoicesNames.WEAVIATE:

            artifact = self._guard_weaviate_modifications(
                connection=connection,
                raw_query=raw_query
            )

        else:
            logger.error(f"Unsupported NoSQL DB type: {nosql_db_type}")
            return None

        if artifact:
            return artifact

        else:
            return None

    def _guard_unix_file_system_modifications(
        self,
        connection,
        raw_query: str
    ):
        from apps.datasource_file_systems.models import (
            DataSourceFileSystem
        )

        from apps.beamguard.utils import (
            BeamGuardArtifactTypesNames,
            BeamGuardConfirmationStatusesNames,
        )

        connection: DataSourceFileSystem

        unauthorized_keyword_found = False
        unauthorized_keywords_list = []

        for keyword in UNIX_FILE_SYSTEM_GUARDED_KEYWORDS:

            if keyword in raw_query.lower():
                unauthorized_keyword_found = True
                unauthorized_keywords_list.append(keyword)

        if not unauthorized_keyword_found and not unauthorized_keywords_list:
            return None

        logger.warning(f"Unauthorized keyword found in Unix file system query: {raw_query}")

        try:
            artifact = BeamGuardArtifact.objects.create(
                assistant=self.assistant,
                chat=self.chat,
                name="Unauthorized Keyword Found",
                raw_query=raw_query,
                metadata={
                    "assistant": {
                        "assistant_name": self.assistant.name,
                        "assistant_description": self.assistant.description,
                    },
                    "data_source": {
                        "data_source_type": "File System",
                        "os_type": connection.os_type,
                        "name": connection.name,
                        "dbms_type": f"File System - {connection.os_type}",
                        "description": connection.description,
                        "host_url": connection.host_url,
                        "port": connection.port,
                    },
                    "query": {
                        "raw_query": raw_query,
                        "problematic_keywords": unauthorized_keywords_list,
                    }
                },
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
                type=BeamGuardArtifactTypesNames.FILE_SYSTEM,
                # sql_connection_object=None,
                # nosql_connection_object=None,
                file_system_connection_object=connection
            )
            artifact.save()

            logger.info(f"BeamGuard artifact created: {artifact}")

            return artifact

        except Exception as e:
            logger.error(f"Failed to create BeamGuard artifact: {e}")

            return None

    def guard_file_system_modifications(self, connection_id: int, raw_query: str):
        from apps.datasource_file_systems.models import (
            DataSourceFileSystem
        )

        connection = DataSourceFileSystem.objects.get(
            id=connection_id
        )

        os_type = connection.os_type

        if os_type == DataSourceFileSystemsOsTypeNames.LINUX or DataSourceFileSystemsOsTypeNames.MACOS:

            artifact = self._guard_unix_file_system_modifications(
                connection=connection,
                raw_query=raw_query
            )

        else:
            logger.error(f"Unsupported OS type: {os_type}")
            return None

        if artifact:
            return artifact

        else:
            return None

    ############################################################################################################
    # ARTIFACT ABSOLUTION
    ############################################################################################################

    @staticmethod
    def _authorize_and_absolve_sql_artifact(artifact: BeamGuardArtifact):
        if artifact.sql_connection_object.dbms_type == DBMSChoicesNames.MYSQL:

            xc_mysql = MySQLExecutor(
                connection=artifact.sql_connection_object
            )

            output = xc_mysql.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute MySQL query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed MySQL query: {artifact.raw_query}")

            return True

        elif artifact.sql_connection_object.dbms_type == DBMSChoicesNames.POSTGRESQL:

            xc_postgresql = PostgresSQLExecutor(
                connection=artifact.sql_connection_object
            )

            output = xc_postgresql.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute PostgreSQL query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed PostgreSQL query: {artifact.raw_query}")

            return True

        elif artifact.sql_connection_object.dbms_type == DBMSChoicesNames.MSSQL:

            xc_mssql = MSSQLExecutor(
                connection=artifact.sql_connection_object
            )

            output = xc_mssql.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute MSSQL query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed MSSQL query: {artifact.raw_query}")

            return True

        elif artifact.sql_connection_object.dbms_type == DBMSChoicesNames.ORACLE:

            xc_oracle = OracleDBExecutor(
                connection=artifact.sql_connection_object
            )

            output = xc_oracle.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute Oracle query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed Oracle query: {artifact.raw_query}")

            return True

        elif artifact.sql_connection_object.dbms_type == DBMSChoicesNames.MARIADB:

            xc_mariadb = MariaDBExecutor(
                connection=artifact.sql_connection_object
            )

            output = xc_mariadb.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute MariaDB query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed MariaDB query: {artifact.raw_query}")

            return True

        else:
            logger.error(f"Unsupported DBMS type: {artifact.sql_connection_object.dbms_type}")

            return False

    @staticmethod
    def _authorize_and_absolve_nosql_artifact(artifact: BeamGuardArtifact):

        if artifact.nosql_connection_object.nosql_db_type == NoSQLDatabaseChoicesNames.COUCHBASE:
            xc_couchbase = CouchbaseNoSQLExecutor(
                connection=artifact.nosql_connection_object
            )

            output = xc_couchbase.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute Couchbase N1QL query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed Couchbase N1QL query: {artifact.raw_query}")

            return True

        elif artifact.nosql_connection_object.nosql_db_type == NoSQLDatabaseChoicesNames.MONGODB:

            xc_mongodb = MongoDBNoSQLExecutor(
                connection=artifact.nosql_connection_object
            )

            output = xc_mongodb.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute MongoDB query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed MongoDB query: {artifact.raw_query}")

            return True

        elif artifact.nosql_connection_object.nosql_db_type == NoSQLDatabaseChoicesNames.REDIS:

            xc_redis = RedisNoSQLExecutor(
                connection=artifact.nosql_connection_object
            )

            output = xc_redis.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute Redis query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed Redis query: {artifact.raw_query}")

            return True

        elif artifact.nosql_connection_object.nosql_db_type == NoSQLDatabaseChoicesNames.ELASTICSEARCH:

            xc_elasticsearch = ElasticSearchNoSQLExecutor(
                connection=artifact.nosql_connection_object
            )

            output = xc_elasticsearch.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute ElasticSearch query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed ElasticSearch query: {artifact.raw_query}")

            return True

        elif artifact.nosql_connection_object.nosql_db_type == NoSQLDatabaseChoicesNames.NEO4J:

            xc_neo4j = Neo4JNoSQLExecutor(
                connection=artifact.nosql_connection_object
            )

            output = xc_neo4j.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute Neo4j query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed Neo4j query: {artifact.raw_query}")

            return True

        elif artifact.nosql_connection_object.nosql_db_type == NoSQLDatabaseChoicesNames.WEAVIATE:

            xc_weaviate = WeaviateNoSQLExecutor(
                connection=artifact.nosql_connection_object
            )

            output = xc_weaviate.execute_write(
                query=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute Weaviate query: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed Weaviate query: {artifact.raw_query}")

            return True

        else:
            logger.error(f"Unsupported NoSQL DB type: {artifact.nosql_connection_object.nosql_db_type}")

            return False

    @staticmethod
    def _authorize_and_absolve_file_system_artifact(artifact: BeamGuardArtifact):

        from apps.core.file_systems.file_systems_executor import (
            FileSystemsExecutor
        )

        if (
            artifact.file_system_connection_object.os_type == DataSourceFileSystemsOsTypeNames.LINUX or
            artifact.file_system_connection_object.os_type == DataSourceFileSystemsOsTypeNames.MACOS
        ):
            xc_unix_file_system = FileSystemsExecutor(
                connection=artifact.file_system_connection_object
            )

            output = xc_unix_file_system.execute_file_system_command_set(
                commands=artifact.raw_query
            )

            if output.get("status", False) is False:
                logger.error(f"Failed to execute Unix file system command set: {artifact.raw_query}")

                return False

            logger.info(f"Successfully executed Unix file system command set: {artifact.raw_query}")

            return True

        else:
            logger.error(f"Unsupported OS type: {artifact.file_system_connection_object.os_type}")

            return False

    @staticmethod
    def reject_and_discard_artifact(artifact_id: int):
        from apps.beamguard.utils import (
            BeamGuardConfirmationStatusesNames,
        )

        artifact = BeamGuardArtifact.objects.get(
            id=artifact_id
        )

        if not artifact:
            logger.error(f"BeamGuard artifact not found: {artifact_id}")

            return False

        if artifact.confirmation_status == BeamGuardConfirmationStatusesNames.REJECTED:
            logger.warning(f"BeamGuard artifact already rejected: {artifact_id}")

            return False

        if artifact.confirmation_status == BeamGuardConfirmationStatusesNames.CONFIRMED:
            logger.warning(f"BeamGuard artifact is confirmed, confirmations can't be reverted: {artifact_id}")

            return False

        artifact.confirmation_status = BeamGuardConfirmationStatusesNames.REJECTED
        artifact.processed_at = timezone.now()

        artifact.save()

        logger.info(f"BeamGuard artifact has been rejected and discarded: {artifact_id}")

        return True

    @staticmethod
    def authorize_and_absolve_artifact(artifact_id: int):
        from apps.beamguard.utils import (
            BeamGuardConfirmationStatusesNames,
        )

        artifact = BeamGuardArtifact.objects.get(
            id=artifact_id
        )

        if not artifact:
            logger.error(f"BeamGuard artifact not found: {artifact_id}")

            return False

        if artifact.confirmation_status == BeamGuardConfirmationStatusesNames.CONFIRMED:
            logger.warning(f"BeamGuard artifact already confirmed: {artifact_id}")

            return False

        if artifact.confirmation_status == BeamGuardConfirmationStatusesNames.REJECTED:
            logger.warning(f"BeamGuard artifact is rejected, rejections can't be reverted: {artifact_id}")

            return False

        artifact.confirmation_status = BeamGuardConfirmationStatusesNames.CONFIRMED
        artifact.processed_at = timezone.now()

        if artifact.sql_connection_object:

            absolved = BeamGuardExecutionManager._authorize_and_absolve_sql_artifact(
                artifact=artifact
            )

        elif artifact.nosql_connection_object:

            absolved = BeamGuardExecutionManager._authorize_and_absolve_nosql_artifact(
                artifact=artifact
            )

        elif artifact.file_system_connection_object:

            absolved = BeamGuardExecutionManager._authorize_and_absolve_file_system_artifact(
                artifact=artifact
            )

        else:
            logger.error(f"Unsupported BeamGuard artifact type: {artifact.type}")

            return False

        if absolved:
            logger.info(f"BeamGuard artifact confirmed: {artifact_id}")

            artifact.save()

            return True

        else:
            logger.error(f"Failed to confirm BeamGuard artifact: {artifact_id}")

            return False
