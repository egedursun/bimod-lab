#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-22 02:05:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 02:05:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.urls import path

from apps.binexus.views import (BinexusView_ProcessCreate, BinexusView_ProcessList, BinexusView_ProcessDelete,
                                BinexusView_ProcessDetail, BinexusView_ProcessUpdate, BinexusView_ProcessExecute,
                                BinexusView_EliteAgentDelete, BinexusView_ProcessPurgeData)

app_name = 'binexus'

urlpatterns = [
    path('process/create/', BinexusView_ProcessCreate.as_view(
        template_name="binexus/process/create_binexus_process.html"), name='process_create'),
    path('process/list/', BinexusView_ProcessList.as_view(
        template_name="binexus/process/list_binexus_processes.html"), name='process_list'),
    path('process/delete/<int:pk>/', BinexusView_ProcessDelete.as_view(
        template_name="binexus/process/confirm_delete_binexus_process.html"
    ), name='process_delete'),
    path('process/detail/<int:pk>/', BinexusView_ProcessDetail.as_view(
        template_name="binexus/process/detail_binexus_process.html"
    ), name='process_detail'),
    path('process/update/<int:pk>/', BinexusView_ProcessUpdate.as_view(
        template_name="binexus/process/update_binexus_process.html"
    ), name='process_update'),

    #####

    path('elite_agent/delete/<int:pk>/', BinexusView_EliteAgentDelete.as_view(), name='elite_agent_delete'),
    path('process/purge_data/<int:pk>/', BinexusView_ProcessPurgeData.as_view(), name='process_purge_data'),

    #####

    path('process/execute/<int:pk>/', BinexusView_ProcessExecute.as_view(), name='process_execute'),
]
