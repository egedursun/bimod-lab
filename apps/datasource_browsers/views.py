import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.datasource_browsers.models import BROWSER_TYPES, DataSourceBrowserConnection, DataSourceBrowserBrowsingLog
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CreateBrowserConnectionView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = context_user.organizations.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=organizations)
        context['browser_types'] = BROWSER_TYPES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD BROWSER CONNECTIONS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(user=request.user).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_WEB_BROWSERS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add browser connections."}
            return self.render_to_response(context)
        ##############################

        name = request.POST.get('name')
        description = request.POST.get('description')
        browser_type = request.POST.get('browser_type')
        assistant_id = request.POST.get('assistant')
        data_selectivity = request.POST.get('data_selectivity', 0.5)
        minimum_investigation_sites = request.POST.get('minimum_investigation_sites', 2)
        whitelisted_extensions = request.POST.getlist('whitelisted_extensions[]')
        blacklisted_extensions = request.POST.getlist('blacklisted_extensions[]')

        # reading abilities checkboxes
        ra_javascript = request.POST.get('ra_javascript') == 'on'
        ra_style = request.POST.get('ra_style') == 'on'
        ra_inline_style = request.POST.get('ra_inline_style') == 'on'
        ra_comments = request.POST.get('ra_comments') == 'on'
        ra_links = request.POST.get('ra_links') == 'on'
        ra_meta = request.POST.get('ra_meta') == 'on'
        ra_page_structure = request.POST.get('ra_page_structure') == 'on'
        ra_processing_instructions = request.POST.get('ra_processing_instructions') == 'on'
        ra_embedded = request.POST.get('ra_embedded') == 'on'
        ra_frames = request.POST.get('ra_frames') == 'on'
        ra_forms = request.POST.get('ra_forms') == 'on'
        ra_remove_tags = request.POST.get('ra_remove_tags') == 'on'

        reading_abilities = {
            "javascript": ra_javascript, "style": ra_style, "inline_style": ra_inline_style, "comments": ra_comments,
            "links": ra_links, "meta": ra_meta, "page_structure": ra_page_structure,
            "processing_instructions": ra_processing_instructions, "embedded": ra_embedded, "frames": ra_frames,
            "forms": ra_forms, "remove_tags": ra_remove_tags
        }
        created_by_user = request.user

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            data_source = DataSourceBrowserConnection.objects.create(
                name=name, description=description, browser_type=browser_type, assistant=assistant,
                data_selectivity=data_selectivity, minimum_investigation_sites=minimum_investigation_sites,
                whitelisted_extensions=whitelisted_extensions, blacklisted_extensions=blacklisted_extensions,
                reading_abilities=reading_abilities, created_by_user=created_by_user
            )
            data_source.save()
            print("[CreateBrowserConnectionView.post] Data Source Browser Connection created successfully.")
            messages.success(request, 'Data Source Browser Connection created successfully.')
            return redirect('datasource_browsers:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_browsers:create')
        except Exception as e:
            messages.error(request, f'Error creating Data Source Browser Connection: {e}')
            return redirect('datasource_browsers:create')


class UpdateBrowserConnectionView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = context_user.organizations.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=organizations)
        context['browser_types'] = BROWSER_TYPES
        context['user'] = context_user
        connection_id = kwargs.get('pk')
        context['browser_connection'] = get_object_or_404(DataSourceBrowserConnection, pk=connection_id)
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        # PERMISSION CHECK FOR - UPDATE BROWSER CONNECTIONS
        user_permissions = (UserPermission.active_permissions.filter(user=request.user).all()
                            .values_list('permission_type', flat=True))
        if PermissionNames.UPDATE_WEB_BROWSERS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update browser connections."}
            return self.render_to_response(context)

        connection_id = kwargs.get('pk')
        browser_connection = get_object_or_404(DataSourceBrowserConnection, pk=connection_id)

        name = request.POST.get('name')
        description = request.POST.get('description')
        browser_type = request.POST.get('browser_type')
        assistant_id = request.POST.get('assistant')
        data_selectivity = request.POST.get('data_selectivity', 0.5)
        minimum_investigation_sites = request.POST.get('minimum_investigation_sites', 2)
        whitelisted_extensions = request.POST.getlist('whitelisted_extensions[]')
        blacklisted_extensions = request.POST.getlist('blacklisted_extensions[]')

        # reading abilities checkboxes
        ra_javascript = request.POST.get('ra_javascript') == 'on'
        ra_style = request.POST.get('ra_style') == 'on'
        ra_inline_style = request.POST.get('ra_inline_style') == 'on'
        ra_comments = request.POST.get('ra_comments') == 'on'
        ra_links = request.POST.get('ra_links') == 'on'
        ra_meta = request.POST.get('ra_meta') == 'on'
        ra_page_structure = request.POST.get('ra_page_structure') == 'on'
        ra_processing_instructions = request.POST.get('ra_processing_instructions') == 'on'
        ra_embedded = request.POST.get('ra_embedded') == 'on'
        ra_frames = request.POST.get('ra_frames') == 'on'
        ra_forms = request.POST.get('ra_forms') == 'on'
        ra_remove_tags = request.POST.get('ra_remove_tags') == 'on'

        reading_abilities = {
            "javascript": ra_javascript, "style": ra_style, "inline_style": ra_inline_style, "comments": ra_comments,
            "links": ra_links, "meta": ra_meta, "page_structure": ra_page_structure,
            "processing_instructions": ra_processing_instructions, "embedded": ra_embedded, "frames": ra_frames,
            "forms": ra_forms, "remove_tags": ra_remove_tags
        }
        created_by_user = request.user

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            browser_connection.name = name
            browser_connection.description = description
            browser_connection.browser_type = browser_type
            browser_connection.assistant = assistant
            browser_connection.data_selectivity = data_selectivity
            browser_connection.minimum_investigation_sites = minimum_investigation_sites
            browser_connection.whitelisted_extensions = whitelisted_extensions
            browser_connection.blacklisted_extensions = blacklisted_extensions
            browser_connection.reading_abilities = reading_abilities
            browser_connection.created_by_user = created_by_user
            browser_connection.save()
            messages.success(request, 'Data Source Browser Connection updated successfully.')
            print("[UpdateBrowserConnectionView.post] Data Source Browser Connection updated successfully.")
            return redirect('datasource_browsers:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_browsers:update', pk=connection_id)
        except Exception as e:
            messages.error(request, f'Error updating Data Source Browser Connection: {e}')
            return redirect('datasource_browsers:update', pk=connection_id)


class DeleteBrowserConnectionView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['browser_connection'] = get_object_or_404(DataSourceBrowserConnection, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - DELETE BROWSER CONNECTIONS
        user_permissions = (UserPermission.active_permissions.filter(user=request.user)
                            .all().values_list('permission_type',flat=True))
        if PermissionNames.DELETE_WEB_BROWSERS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to delete browser connections."}
            return self.render_to_response(context)

        browser_connection = get_object_or_404(DataSourceBrowserConnection, pk=self.kwargs['pk'])
        browser_connection.delete()
        messages.success(request, 'Browser Connection deleted successfully.')
        print("[DeleteBrowserConnectionView.post] Browser Connection deleted successfully.")
        return redirect('datasource_browsers:list')


class ListBrowserConnectionsView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        connections_by_organization = {}
        assistants = Assistant.objects.filter(
            organization__in=context_user.organizations.filter(users__in=[context_user])
        )

        for assistant in assistants:
            organization = assistant.organization
            if organization not in connections_by_organization:
                connections_by_organization[organization] = {}
            if assistant not in connections_by_organization[organization]:
                connections_by_organization[organization][assistant] = []

            connections = DataSourceBrowserConnection.objects.filter(assistant=assistant)
            connections_by_organization[organization][assistant].extend(connections)

        context['connections_by_organization'] = connections_by_organization
        context['user'] = context_user
        print("[ListBrowserConnectionsView.get_context_data] Browser Connections listed successfully.")
        return context


class ListBrowsingLogsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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


class DownloadHtmlContentView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        log = get_object_or_404(DataSourceBrowserBrowsingLog, pk=pk)
        response = HttpResponse(log.html_content, content_type='text/html')
        response[
            'Content-Disposition'] = f'attachment; filename="{log.connection.name}_html_content_{log.created_at.strftime("%Y%m%d%H%M%S")}.html"'
        print("[DownloadHtmlContentView.get] HTML content downloaded successfully.")
        return response


class DownloadContextDataView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        log = get_object_or_404(DataSourceBrowserBrowsingLog, pk=pk)
        context_data = json.dumps(log.context_content, indent=4)
        response = HttpResponse(context_data, content_type='application/json')
        response[
            'Content-Disposition'] = f'attachment; filename="{log.connection.name}_context_data_{log.created_at.strftime("%Y%m%d%H%M%S")}.json"'
        print("[DownloadContextDataView.get] Context data downloaded successfully.")
        return response
