#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.urls import path

from apps.data_backups.views import ManageDataBackupsView, DeleteDataBackupView, ReloadBackupView

app_name = 'data_backups'

urlpatterns = [
    path('manage/', ManageDataBackupsView.as_view(
        template_name='data_backups/manage_backups.html'
    ), name='manage'),
    path('delete/<int:backup_id>/', DeleteDataBackupView.as_view(), name='delete'),
    path('reload/<int:backup_id>/', ReloadBackupView.as_view(), name='reload'),
]
