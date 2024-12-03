#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

SSH_CONNECTION_DEFAULT_BANNER_TIMEOUT = 200

DATASOURCE_FILE_SYSTEMS_OS_TYPES = [
    ('linux', 'Linux'),
    ('macos', 'MacOS'),
]


class DataSourceFileSystemsOsTypeNames:
    LINUX = 'linux'
    MACOS = 'macos'


FILE_SYSTEM_ADMIN_LIST = (
    'name',
    'os_type',
    'host_url',
    'port',
    'username',
    'is_read_only'
)

FILE_SYSTEM_ADMIN_FILTER = (
    'os_type',
    'is_read_only'
)

FILE_SYSTEM_ADMIN_SEARCH = (
    'name',
    'host_url',
    'username',
    'ssh_connection_uri'
)
