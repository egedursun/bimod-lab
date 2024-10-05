#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: download_context_data_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: download_context_data_views.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:32:58
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.datasource_browsers.models import DataSourceBrowserBrowsingLog


class DownloadContextDataView(LoginRequiredMixin, View):
    """
    Handles downloading the context data of a specific browsing log.

    This view allows users to download the context data captured during a browsing session. The content is returned as a JSON file.

    Methods:
        get(self, request, pk, *args, **kwargs): Retrieves the context data of the specified browsing log and serves it as a downloadable JSON file.
    """

    def get(self, request, pk, *args, **kwargs):
        log = get_object_or_404(DataSourceBrowserBrowsingLog, pk=pk)
        context_data = json.dumps(log.context_content, indent=4)
        response = HttpResponse(context_data, content_type='application/json')
        response[
            'Content-Disposition'] = f'attachment; filename="{log.connection.name}_context_data_{log.created_at.strftime("%Y%m%d%H%M%S")}.json"'
        print("[DownloadContextDataView.get] Context data downloaded successfully.")
        return response
