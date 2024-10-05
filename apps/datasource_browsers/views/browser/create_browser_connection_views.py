#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_browser_connection_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.datasource_browsers.utils import BROWSER_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateBrowserConnectionView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of a new data source browser connection.

    This view displays a form for creating a browser connection. Upon submission, it validates the input, checks user permissions, and saves the new browser connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including available assistants, browser types, and user details.
        post(self, request, *args, **kwargs): Handles form submission and browser connection creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = context_user.organizations.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=organizations)
        context['browser_types'] = BROWSER_TYPES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - ADD_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_WEB_BROWSERS):
            messages.error(self.request, "You do not have permission to add web browsers.")
            return redirect('datasource_browsers:list')
        ##############################

        name = request.POST.get('name')
        description = request.POST.get('description')
        browser_type = request.POST.get('browser_type')
        assistant_id = request.POST.get('assistant')
        data_selectivity = request.POST.get('data_selectivity', 0.5)
        minimum_investigation_sites = request.POST.get('minimum_investigation_sites', 2)

        whitelisted_extensions = request.POST.getlist('whitelisted_extensions[]')
        blacklisted_extensions = request.POST.getlist('blacklisted_extensions[]')

        # clean white listed extensions
        cleaned_whitelisted_extensions = []
        for ext in whitelisted_extensions:
            ext = ext.strip()
            if ext != '' and ext is not None and ext != 'None':
                cleaned_whitelisted_extensions.append(ext)
        whitelisted_extensions = cleaned_whitelisted_extensions

        # clean black listed extensions
        cleaned_blacklisted_extensions = []
        for ext in blacklisted_extensions:
            ext = ext.strip()
            if ext != '' and ext is not None and ext != 'None':
                cleaned_blacklisted_extensions.append(ext)
        blacklisted_extensions = cleaned_blacklisted_extensions

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
