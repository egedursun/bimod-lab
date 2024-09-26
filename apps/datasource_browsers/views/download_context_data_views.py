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
