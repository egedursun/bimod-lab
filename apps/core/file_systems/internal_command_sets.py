#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

class DataSourceFileSystemsOsTypeNames:
    LINUX = 'linux'
    MACOS = 'macos'


LIST_DIRECTORY_RECURSIVE = 'list_directory_recursive'

INTERNAL_COMMAND_SETS = {
    LIST_DIRECTORY_RECURSIVE: {
        'description': 'List directory contents recursively',
        DataSourceFileSystemsOsTypeNames.LINUX: """
        find / -type d \( \
        ! -path "/proc*" -a ! -path "/sys*" -a ! -path "/dev*" -a ! -path "/run*" -a \
        ! -path "/tmp*" -a ! -path "/lib*" -a ! -path "/usr/lib*" -a ! -path "/usr/local*" -a \
        ! -path "/usr/src*" -a ! -path "/usr/share*" -a ! -path "/usr/include*" -a \
        ! -path "/usr/portage*" -a ! -path "/opt*" -a ! -path "/boot*" -a ! -path "/snap*" -a \
        ! -path "/mnt*" -a ! -path "/media*" -a ! -path "/var/cache*" -a ! -path "/var/lib/docker*" -a \
        ! -path "/var/lib/containers*" -a ! -path "/var/lib/rpm*" -a ! -path "/var/lib/dpkg*" -a \
        ! -path "/var/snap*" -a ! -path "/var/backups*" -a ! -path "/var/tmp*" -a ! -path "/var/log*" -a \
        ! -path "/sys/kernel/debug*" -a ! -path "/sys/fs/cgroup*" -a ! -path "/srv*" -a \
        ! -path "/home/*/.cache*" -a ! -path "/home/*/.local*" -a \
        ! -path "/home/*/.npm*" -a ! -path "/home/*/.yarn*" -a ! -path "/home/*/.gem*" -a \
        ! -path "*/node_modules*" -a ! -path "*/.git*" -a ! -path "*/.svn*" -a ! -path "*/.hg*" -a \
        ! -path "*/venv*" -a ! -path "*/env*" -a ! -path "*/__pycache__*" -a \
        ! -path "*/.maven*" -a ! -path "*/.gradle*" -a ! -path "*/.cache*" -a \
        ! -path "*/target*" -a ! -path "*/build*" -a ! -path "*/dist*" -a ! -path "*/.*" \)
        """,

        DataSourceFileSystemsOsTypeNames.MACOS: """
        find / -type d \( \
        ! -path "/proc*" -a ! -path "/sys*" -a ! -path "/dev*" -a ! -path "/run*" -a \
        ! -path "/tmp*" -a ! -path "/lib*" -a ! -path "/usr/lib*" -a ! -path "/usr/local*" -a \
        ! -path "/usr/src*" -a ! -path "/usr/share*" -a ! -path "/usr/include*" -a \
        ! -path "/usr/portage*" -a ! -path "/opt*" -a ! -path "/boot*" -a ! -path "/snap*" -a \
        ! -path "/mnt*" -a ! -path "/media*" -a ! -path "/var/cache*" -a ! -path "/var/lib/docker*" -a \
        ! -path "/var/lib/containers*" -a ! -path "/var/lib/rpm*" -a ! -path "/var/lib/dpkg*" -a \
        ! -path "/var/snap*" -a ! -path "/var/backups*" -a ! -path "/var/tmp*" -a ! -path "/var/log*" -a \
        ! -path "/sys/kernel/debug*" -a ! -path "/sys/fs/cgroup*" -a ! -path "/srv*" -a \
        ! -path "/home/*/.cache*" -a ! -path "/home/*/.local*" -a \
        ! -path "/home/*/.npm*" -a ! -path "/home/*/.yarn*" -a ! -path "/home/*/.gem*" -a \
        ! -path "*/node_modules*" -a ! -path "*/.git*" -a ! -path "*/.svn*" -a ! -path "*/.hg*" -a \
        ! -path "*/venv*" -a ! -path "*/env*" -a ! -path "*/__pycache__*" -a \
        ! -path "*/.maven*" -a ! -path "*/.gradle*" -a ! -path "*/.cache*" -a \
        ! -path "*/target*" -a ! -path "*/build*" -a ! -path "*/dist*" -a ! -path "*/.*" \)
        """,
    }
}
