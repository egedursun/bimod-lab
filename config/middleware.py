#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: middleware.py
#  Last Modified: 2024-10-05 15:31:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:30:49
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import logging

from auth.models import Profile
from config.consts.loading_bar_content import CONTENT_MIX
from config.settings import SUFFIX_ANY

logger = logging.getLogger(__name__)

HTTP_STATUS_QUERY_TAG = 'http_status'
HTTP_STATUS_ERROR_TAG_VALUE = 'error'


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):

        # Skip authentication check for excluded pages
        for excluded_page in settings.EXCLUDED_PAGES:
            if SUFFIX_ANY in excluded_page:
                if request.path.startswith(excluded_page.replace(SUFFIX_ANY, "")[:-1]):
                    return None
            else:
                if request.path == excluded_page:
                    return None

        if not request.user.is_anonymous:
            user_data: User = request.user
            user_profile: Profile = user_data.profile

            if user_data.is_superuser:
                if user_data.is_staff:
                    return None
                if not user_profile.is_accredited_by_staff:
                    return redirect('landing:not_accredited')

        # If the user is not authenticated and the page is not the login page, redirect to login
        if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
            return redirect(settings.LOGIN_URL)
        return None


class AppendSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.path.endswith('/')
            and not request.path.startswith('/api/')
            and not request.path.startswith('/app/export_assistants/api/v1/export')
            and not request.path.startswith('/app/export_leanmods/api/v1/export')
            and not request.path.startswith('/app/export_orchestrations/api/v1/export')):
            return HttpResponsePermanentRedirect(request.path + '/')
        return self.get_response(request)


class LoadingBarMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.render()
            content = response.content.decode()
            loading_bar_html = CONTENT_MIX
            response.content = content.replace('</body>', loading_bar_html + '</body>')
        return response
