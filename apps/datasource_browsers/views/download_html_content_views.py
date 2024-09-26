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
