#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: download_html_content_views.py
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

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.datasource_browsers.models import (
    DataSourceBrowserBrowsingLog
)

logger = logging.getLogger(__name__)


class BrowserView_BrowserLogDownloadHTML(LoginRequiredMixin, View):
    def get(
        self,
        request,
        pk,
        *args,
        **kwargs
    ):
        log = get_object_or_404(
            DataSourceBrowserBrowsingLog,
            pk=pk
        )

        response = HttpResponse(
            log.html_content,
            content_type='text/html'
        )

        response[
            'Content-Disposition'
        ] = f'attachment; filename="{log.connection.name}_html_content_{log.created_at.strftime("%Y%m%d%H%M%S")}.html"'

        logger.info(f"User: {request.user} - Browser Log HTML Content: {log.connection.name} - Downloaded.")

        return response
