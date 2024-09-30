#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: __init__.py
#  Last Modified: 2024-09-26 18:15:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:18:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.
from django.contrib.auth.models import User

from .create_assistant_views import *
from .delete_assistant_views import *
from .update_assistant_views import *
from .list_assistants_views import *

from ..._services.data_backups.data_backup_executor import DataBackupExecutor
from ...data_backups.models import DataBackup

##############################################################################################################
##############################################################################################################

# test
"""
x = DataBackupExecutor.BackupNERInstance(responsible_user=User.objects.get(username="admin"),
                                      organization=Organization.objects.get(
                                          pk=2))
error_message = x.backup_ner_instances("backup_name", "password")
# error_message = DataBackupExecutor.restore(DataBackup.objects.get(backup_name="backup_name1"), "password")
if error_message is not None:
    print(error_message)
"""

##############################################################################################################
##############################################################################################################
