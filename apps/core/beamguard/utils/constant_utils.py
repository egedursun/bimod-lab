#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-12-02 01:24:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:24:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

MYSQL_GUARDED_KEYWORDS = [
    "UPDATE",
    "ALTER",
    "RENAME",
    "DELETE",
    "DROP",
    "TRUNCATE",
    "REVOKE",
]

POSTGRESQL_GUARDED_KEYWORDS = [
    "UPDATE",
    "ALTER",
    "RENAME",
    "DELETE",
    "DROP",
    "TRUNCATE",
    "DISCARD",
    "REVOKE",
]

N1QL_GUARDED_KEYWORDS = [
    "UPDATE",
    "MERGE",
    "ALTER",
    "GRANT",
    "REVOKE",
    "DELETE",
    "UNSET",
    "DROP",
]

UNIX_FILE_SYSTEM_GUARDED_KEYWORDS = [
    # File and Directory Operations
    "rm",
    "rmdir",
    "unlink",
    "truncate",
    "ln",

    # File Permission and Ownership
    "chmod",
    "chown",
    "chgrp",

    # Data Overwriting and Secure Deletion
    "shred",
    "dd",
    "tee",

    # Filesystem and Disk Management
    "mkfs",
    "fsck",
    "parted",
    "fdisk",
    "mklabel",
    "mount",
    "umount",
    "xfs_repair",

    # Process and System Management
    "kill",
    "pkill",
    "killall",
    "systemctl",
    "service",
    "swapoff",

    # Device and Network Operations
    "losetup",
    "iptables",
    "ip",
    "ifconfig",
    "netstat",

    # Package and Software Management
    "apt",
    "yum",
    "dnf",
    "zypper",
    "pacman",
    "brew",

    # User and System Account Management
    "useradd",
    "usermod",
    "userdel",
    "passwd",

    # System Configuration and Power
    "reboot",
    "shutdown",
    "halt",
    "poweroff",
]
