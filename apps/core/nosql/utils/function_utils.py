#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
#  Last Modified: 2024-10-10 16:19:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-10 16:19:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.datasource_nosql.utils import NoSQLDatabaseChoicesNames


def before_execute_nosql_query(connection: NoSQLDatabaseConnection):
    old_schema_json = connection.schema_data_json
    new_schema = {}
    if connection.nosql_db_type == NoSQLDatabaseChoicesNames.COUCHBASE:
        new_schema = connection.retrieve_couchbase_schema()
    if new_schema != old_schema_json:
        connection.schema_data_json = new_schema
        connection.save()


def can_write_to_database(connection: NoSQLDatabaseConnection):
    return not connection.is_read_only
