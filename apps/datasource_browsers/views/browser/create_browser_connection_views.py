#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant

from apps.datasource_browsers.models import (
    DataSourceBrowserConnection
)

from apps.datasource_browsers.utils import (
    BROWSER_TYPES,
    BrowserTypesNames
)

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_BROWSERS_PER_ASSISTANT
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BrowserView_BrowserCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            orgs = context_user.organizations.filter(
                users__in=[context_user]
            )

            context['assistants'] = Assistant.objects.filter(
                organization__in=orgs
            )

            context['user'] = context_user

        except Exception as e:
            logger.error(f"User: {context_user} - Data Source Browser Connection - Create Error: {e}")
            messages.error(self.request, 'An error occurred while creating Data Source Browser Connection.')

            return context

        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - ADD_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_WEB_BROWSERS
        ):
            messages.error(self.request, "You do not have permission to add web browsers.")
            return redirect('datasource_browsers:list')
        ##############################

        browser_name = request.POST.get('name')
        description = request.POST.get('description')
        browser_type = BrowserTypesNames.GOOGLE
        agent_id = request.POST.get('assistant')

        browser_selectivity = request.POST.get('data_selectivity', 0.5)
        min_investigation_websites = request.POST.get('minimum_investigation_sites', 2)

        whitelisted_exts = request.POST.getlist('whitelisted_extensions[]')
        blacklisted_exts = request.POST.getlist('blacklisted_extensions[]')

        whitelisted_exts_cleaned = []

        for ext in whitelisted_exts:
            ext = ext.strip()
            if (
                ext != '' and ext is not None and
                ext != 'None'
            ):
                whitelisted_exts_cleaned.append(ext)

        whitelisted_exts = whitelisted_exts_cleaned

        blacklisted_exts_cleaned = []

        for ext in blacklisted_exts:
            ext = ext.strip()

            if (
                ext != '' and ext is not None and
                ext != 'None'
            ):
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
            "javascript": ra_javascript,
            "style": ra_style,
            "inline_style": ra_inline_style,
            "comments": ra_comments,
            "links": ra_links,
            "meta": ra_meta,
            "page_structure": ra_page_structure,
            "processing_instructions": ra_processing_instructions,
            "embedded": ra_embedded,
            "frames": ra_frames,
            "forms": ra_forms,
            "remove_tags": ra_remove_tags
        }

        created_by_user = request.user

        try:
            assistant = Assistant.objects.get(
                id=agent_id
            )

            n_browsers = assistant.datasourcebrowserconnection_set.count()

            if n_browsers > MAX_BROWSERS_PER_ASSISTANT:
                messages.error(request,
                               f'Assistant has reached the maximum number of browser connections ({MAX_BROWSERS_PER_ASSISTANT}).')

                return redirect('datasource_browsers:create')

            info_feed = DataSourceBrowserConnection.objects.create(
                name=browser_name,
                description=description,
                browser_type=browser_type,
                assistant=assistant,
                data_selectivity=browser_selectivity,
                minimum_investigation_sites=min_investigation_websites,
                whitelisted_extensions=whitelisted_exts,
                blacklisted_extensions=blacklisted_exts,
                reading_abilities=capabilities,
                created_by_user=created_by_user
            )

            info_feed.save()

            logger.info(f"User: {request.user} - Data Source Browser Connection: {info_feed.name} - Created.")
            messages.success(request, 'Data Source Browser Connection created successfully.')

            return redirect('datasource_browsers:list')

        except Assistant.DoesNotExist:
            logger.error('Invalid assistant selected.')
            messages.error(request, 'Invalid assistant selected.')

            return redirect('datasource_browsers:create')

        except Exception as e:
            logger.error(f'Error creating Data Source Browser Connection: {e}')
            messages.error(request, f'Error creating Data Source Browser Connection: {e}')

            return redirect('datasource_browsers:create')
