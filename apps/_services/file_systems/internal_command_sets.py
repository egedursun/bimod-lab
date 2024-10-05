#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: internal_command_sets.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

class DataSourceFileSystemsOsTypeNames:
    LINUX = 'linux'
    MACOS = 'macos'


LIST_DIRECTORY_RECURSIVE = 'list_directory_recursive'
INTERNAL_COMMAND_SETS = {
    LIST_DIRECTORY_RECURSIVE: {
        'description': 'List directory contents recursively',
        DataSourceFileSystemsOsTypeNames.LINUX: 'ls -R ../',
        DataSourceFileSystemsOsTypeNames.MACOS: 'ls -R ../',
    }
}
