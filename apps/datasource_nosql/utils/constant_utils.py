#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-12 13:19:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:19:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


class NoSQLOperationTypesNames:
    READ = 'read'
    WRITE = 'write'


NOSQL_DATABASE_CHOICES = [
    ('couchbase', 'Couchbase'),
]


class NoSQLDatabaseChoicesNames:
    COUCHBASE = 'couchbase'

    @staticmethod
    def as_list():
        return [
            NoSQLDatabaseChoicesNames.COUCHBASE,
        ]


NOSQL_DATABASE_ADMIN_LIST = ('id', 'assistant', 'nosql_db_type', 'name', 'bucket_name', 'is_read_only', 'created_at')
NOSQL_DATABASE_ADMIN_FILTER = ('nosql_db_type', 'created_at')
NOSQL_DATABASE_ADMIN_SEARCH = ('name', 'bucket_name', 'is_read_only')

NOSQL_QUERY_ADMIN_LIST = ('id', 'database_connection', 'name', 'description', 'created_at', 'updated_at')
NOSQL_QUERY_ADMIN_FILTER = ('created_at', 'updated_at')
NOSQL_QUERY_ADMIN_SEARCH = ('name', 'description')
RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED = 1000
VALUE_TRUNCATION_PREFIX_LENGTH = RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED // 2
VALUE_TRUNCATION_SUFFIX_LENGTH = RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED // 2
RETRIEVE_NOSQL_SCHEMA_MAX_DEPTH_ALLOWED = 10
DEFAULT_SCHEMA_SAMPLING_LIMIT = 100
NOSQL_KV_TIMOUT_CONSTANT = 30  # seconds
NOSQL_CONNECT_TIMOUT_CONSTANT = 30  # seconds
NOSQL_QUERY_TIMOUT_CONSTANT = 30  # seconds
