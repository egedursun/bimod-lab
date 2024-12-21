#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

SQL_DBMS_PROVIDERS = {
    "POSTGRESQL": {
        "code": "postgresql",
        "name": "PostgreSQL"
    },
    "MYSQL": {
        "code": "mysql",
        "name": "MySQL"
    },
    "MSSQL": {
        "code": "mssql",
        "name": "Microsoft SQL Server"
    },
    "ORACLE": {
        "code": "oracle",
        "name": "Oracle"
    },
    "MARIADB": {
        "code": "mariaDB",
        "name": "MariaDB"
    },
}


INTRINSIC_MAXIMUM_QUERY_RECORD_LIMIT = 1000


class SQLKeywords:
    LIMIT = "LIMIT"
