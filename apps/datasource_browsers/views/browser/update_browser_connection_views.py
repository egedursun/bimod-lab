#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_browser_connection_views.py
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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.datasource_browsers.utils import BROWSER_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BrowserView_BrowserUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            organizations = context_user.organizations.filter(users__in=[context_user])
            context['assistants'] = Assistant.objects.filter(organization__in=organizations)
            context['browser_types'] = BROWSER_TYPES
            context['user'] = context_user
            connection_id = kwargs.get('pk')
            context['browser_connection'] = get_object_or_404(DataSourceBrowserConnection, pk=connection_id)
        except Exception as e:
            logger.error(f"User: {context_user} - Data Source Browser Connection - Update Error: {e}")
            messages.error(self.request, 'An error occurred while updating Data Source Browser Connection.')
            return context

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_WEB_BROWSERS):
            messages.error(self.request, "You do not have permission to update web browsers.")
            return redirect('datasource_browsers:list')
        ##############################

        c_id = kwargs.get('pk')
        browser_c = get_object_or_404(DataSourceBrowserConnection, pk=c_id)

        browser_name = request.POST.get('name')
        description = request.POST.get('description')
        browser_type = request.POST.get('browser_type')
        agent_id = request.POST.get('assistant')
        browser_selecitivity = request.POST.get('data_selectivity', 0.5)
        min_website_investigations = request.POST.get('minimum_investigation_sites', 2)
        whitelisted_exts = request.POST.getlist('whitelisted_extensions[]')
        blacklisted_exts = request.POST.getlist('blacklisted_extensions[]')

        whitelisted_exts_cleaned = []
        for ext in whitelisted_exts:
            ext = ext.strip()
            if ext != '' and ext is not None and ext != 'None':
                whitelisted_exts_cleaned.append(ext)
        whitelisted_exts = whitelisted_exts_cleaned

        blacklisted_exts_cleaned = []
        for ext in blacklisted_exts:
            ext = ext.strip()
            if ext != '' and ext is not None and ext != 'None':
                blacklisted_exts_cleaned.append(ext)
        blacklisted_exts = blacklisted_exts_cleaned

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

        capabilities = {
            "javascript": ra_javascript, "style": ra_style, "inline_style": ra_inline_style, "comments": ra_comments,
            "links": ra_links, "meta": ra_meta, "page_structure": ra_page_structure,
            "processing_instructions": ra_processing_instructions, "embedded": ra_embedded, "frames": ra_frames,
            "forms": ra_forms, "remove_tags": ra_remove_tags
        }
        created_by_user = request.user

        try:
            assistant = Assistant.objects.get(id=agent_id)
            browser_c.name = browser_name
            browser_c.description = description
            browser_c.browser_type = browser_type
            browser_c.assistant = assistant
            browser_c.data_selectivity = browser_selecitivity
            browser_c.minimum_investigation_sites = min_website_investigations
            browser_c.whitelisted_extensions = whitelisted_exts
            browser_c.blacklisted_extensions = blacklisted_exts
            browser_c.reading_abilities = capabilities
            browser_c.created_by_user = created_by_user
            browser_c.save()
            logger.info(f"User: {request.user} - Data Source Browser Connection: {browser_c.name} - Updated.")
            messages.success(request, 'Data Source Browser Connection updated successfully.')
            return redirect('datasource_browsers:list')
        except Assistant.DoesNotExist:
            logger.error('Invalid assistant selected.')
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_browsers:update', pk=c_id)
        except Exception as e:
            logger.error(f'Error updating Data Source Browser Connection: {e}')
            messages.error(request, f'Error updating Data Source Browser Connection: {e}')
            return redirect('datasource_browsers:update', pk=c_id)
