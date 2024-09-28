from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListBrowsingLogsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of browsing logs for a specific browser connection.

    This view allows users to search and paginate through browsing logs associated with a specific browser connection. It supports filtering logs based on a search query.

    Methods:
        get_context_data(self, **kwargs): Retrieves the browsing logs for the specified browser connection, applies search filters, and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_WEB_BROWSERS):
            messages.error(self.request, "You do not have permission to list web browsers.")
            return context
        ##############################

        connection_id = kwargs.get('pk')
        browser_connection = get_object_or_404(DataSourceBrowserConnection, pk=connection_id)
        context['browser_connection'] = browser_connection

        logs = browser_connection.logs.all()
        search_query = self.request.GET.get('search', '')
        if search_query:
            logs = logs.filter(action__icontains=search_query) | logs.filter(
                html_content__icontains=search_query) | logs.filter(
                context_content__icontains=search_query) | logs.filter(log_content__icontains=search_query)

        paginator = Paginator(logs, 10)  # Show 10 logs per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['search_query'] = search_query
        print("[ListBrowsingLogsView.get_context_data] Browser Browsing Logs listed successfully.")
        return context
