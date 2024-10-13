#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#


class SQLOperationTypesNames:
    READ = 'read'
    WRITE = 'write'


DBMS_CHOICES = [
    ('postgresql', 'PostgreSQL'),
    ('mysql', 'MySQL'),
]


class DBMSChoicesNames:
    POSTGRESQL = 'postgresql'
    MYSQL = 'mysql'


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

SQL_DATABASE_ADMIN_LIST = ('id', 'assistant', 'dbms_type', 'name', 'database_name', 'is_read_only', 'created_at')
SQL_DATABASE_ADMIN_FILTER = ('dbms_type', 'created_at')
SQL_DATABASE_ADMIN_SEARCH = ('name', 'database_name', 'is_read_only')

SQL_QUERY_ADMIN_LIST = ('id', 'database_connection', 'name', 'description', 'created_at', 'updated_at')
SQL_QUERY_ADMIN_FILTER = ('created_at', 'updated_at')
SQL_QUERY_ADMIN_SEARCH = ('name', 'description')
