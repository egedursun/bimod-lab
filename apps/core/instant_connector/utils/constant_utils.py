#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-12-04 00:38:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-28 14:24:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
class InstantConnectionTypes:
    SQL = "sql"
    NOSQL = "nosql"
    SERVER = "server"

    @staticmethod
    def get_sql_valid_subtypes():
        return [
            "postgresql",
            "mysql",
            "mssql",
            "oracle",
            "mariadb"
        ]

    @staticmethod
    def get_nosql_valid_subtypes():
        return [
            "mongodb",
            "couchbase",
            "elasticsearch",
            "neo4j",
            "weaviate",
            "redis",
        ]

    @staticmethod
    def get_server_valid_subtypes():
        return [
            "ssh",
        ]
