#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: download_html_content_views.py
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
#  File: download_html_content_views.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:33:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.datasource_browsers.models import DataSourceBrowserBrowsingLog


class DownloadHtmlContentView(LoginRequiredMixin, View):
    """
    Handles downloading the HTML content of a specific browsing log.

    This view allows users to download the HTML content captured during a browsing session. The content is returned as an HTML file.

    Methods:
        get(self, request, pk, *args, **kwargs): Retrieves the HTML content of the specified browsing log and serves it as a downloadable HTML file.
    """

    def get(self, request, pk, *args, **kwargs):
        log = get_object_or_404(DataSourceBrowserBrowsingLog, pk=pk)
        response = HttpResponse(log.html_content, content_type='text/html')
        response[
            'Content-Disposition'] = f'attachment; filename="{log.connection.name}_html_content_{log.created_at.strftime("%Y%m%d%H%M%S")}.html"'
        print("[DownloadHtmlContentView.get] HTML content downloaded successfully.")
        return response
