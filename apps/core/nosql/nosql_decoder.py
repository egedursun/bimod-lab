#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_decoder.py
#  Last Modified: 2024-10-10 16:20:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-10 16:20:09
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

from apps.core.nosql.nosql_executor import (
    CouchbaseNoSQLExecutor,
    ElasticSearchNoSQLExecutor,
    MongoDBNoSQLExecutor,
    Neo4JNoSQLExecutor,
    RedisNoSQLExecutor,
    WeaviateNoSQLExecutor
)

from apps.core.nosql.utils import (
    NOSQL_DBMS_PROVIDERS
)

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection
)

logger = logging.getLogger(__name__)


class InternalNoSQLClient:
    @staticmethod
    def get(connection: NoSQLDatabaseConnection):
        if connection.nosql_db_type == NOSQL_DBMS_PROVIDERS["COUCHBASE"]["code"]:
            logger.info(f"Creating Couchbase NoSQL client for connection: {connection.name}")

            return CouchbaseNoSQLExecutor(
                connection=connection
            )

        elif connection.nosql_db_type == NOSQL_DBMS_PROVIDERS["ELASTICSEARCH"]["code"]:
            logger.info(f"Creating ElasticSearch NoSQL client for connection: {connection.name}")

            return ElasticSearchNoSQLExecutor(
                connection=connection
            )

        elif connection.nosql_db_type == NOSQL_DBMS_PROVIDERS["MONGODB"]["code"]:
            logger.info(f"Creating MongoDB NoSQL client for connection: {connection.name}")

            return MongoDBNoSQLExecutor(
                connection=connection
            )

        elif connection.nosql_db_type == NOSQL_DBMS_PROVIDERS["NEO4J"]["code"]:
            logger.info(f"Creating Neo4J NoSQL client for connection: {connection.name}")

            return Neo4JNoSQLExecutor(
                connection=connection
            )

        elif connection.nosql_db_type == NOSQL_DBMS_PROVIDERS["REDIS"]["code"]:
            logger.info(f"Creating Redis NoSQL client for connection: {connection.name}")

            return RedisNoSQLExecutor(
                connection=connection
            )

        elif connection.nosql_db_type == NOSQL_DBMS_PROVIDERS["WEAVIATE"]["code"]:
            logger.info(f"Creating Weaviate NoSQL client for connection: {connection.name}")

            return WeaviateNoSQLExecutor(
                connection=connection
            )
