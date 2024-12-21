#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import os

from config.settings import BASE_DIR


class SQLOperationTypesNames:
    READ = 'read'
    WRITE = 'write'


DBMS_CHOICES = [
    ('postgresql', 'PostgreSQL'),
    ('mysql', 'MySQL'),
    ('mssql', 'Microsoft SQL Server'),
    ('oracle', 'Oracle'),
    ('mariaDB', 'MariaDB'),
]


class DBMSChoicesNames:
    POSTGRESQL = 'postgresql'
    MYSQL = 'mysql'
    MSSQL = 'mssql'
    ORACLE = 'oracle'
    MARIADB = 'mariaDB'

    @staticmethod
    def as_list():
        return [
            DBMSChoicesNames.POSTGRESQL,
            DBMSChoicesNames.MYSQL,
            DBMSChoicesNames.MSSQL,
            DBMSChoicesNames.ORACLE,
            DBMSChoicesNames.MARIADB,
        ]


POSTGRESQL_SCHEMA_RETRIEVAL_QUERY = f"""
SELECT table_name
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog');
"""

POSTGRESQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY = f"""
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s
"""

MYSQL_SCHEMA_RETRIEVAL_QUERY = f"""
SELECT table_name
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys');
"""

MYSQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY = f"""
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s
"""

MSSQL_TABLES_QUERY = """
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';
"""

MSSQL_COLUMNS_QUERY = """
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = %s;
"""

ORACLE_SCHEMA_RETRIEVAL_QUERY = """
SELECT TABLE_NAME
FROM USER_TABLES
"""

ORACLE_SCHEMA_RETRIEVAL_QUERY_SUPPLY = """
SELECT COLUMN_NAME, DATA_TYPE
FROM USER_TAB_COLUMNS
WHERE UPPER(TABLE_NAME) = :table_name
"""

MARIADB_SCHEMA_RETRIEVAL_QUERY = """
SHOW TABLES;
"""

MARIADB_SCHEMA_RETRIEVAL_QUERY_SUPPLY = """
SHOW COLUMNS FROM `%s`;
"""

SQL_DATABASE_ADMIN_LIST = (
    'id',
    'assistant',
    'dbms_type',
    'name',
    'database_name',
    'is_read_only',
    'created_at'
)
SQL_DATABASE_ADMIN_FILTER = (
    'dbms_type',
    'created_at'
)
SQL_DATABASE_ADMIN_SEARCH = (
    'name',
    'database_name',
    'is_read_only'
)

SQL_QUERY_ADMIN_LIST = (
    'id',
    'database_connection',
    'name',
    'description',
    'created_at',
    'updated_at'
)
SQL_QUERY_ADMIN_FILTER = (
    'created_at',
    'updated_at'
)
SQL_QUERY_ADMIN_SEARCH = (
    'name',
    'description'
)

DEFAULT_SEARCH_RESULTS_SQL_SCHEMA = 10


class OpenAIEmbeddingModels:
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_V2 = "text-embedding-ada-002"


OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS = 3072

VECTOR_INDEX_PATH_SQL_SCHEMAS = os.path.join(
    BASE_DIR,
    'vectors',
    'sql_schema_vectors',
    'sql_schemas'
)
SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST = (
    'sql_database',
    'created_at',
    'updated_at',
)
SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH = (
    'sql_database__database_name',
    'sql_database__name',
    'sql_database__host',
)
SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER = (
    'created_at',
    'updated_at',
)

SQL_SCHEMA_VECTOR_CHUNK_SIZE = 2_000
SQL_SCHEMA_VECTOR_CHUNK_OVERLAP = 1_000
