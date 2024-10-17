#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: session_timeout_middleware.py
#  Last Modified: 2024-10-09 19:28:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:28:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from auth.models import Profile
from config.settings import SUFFIX_ANY


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
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

        if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
            return redirect(settings.LOGIN_URL)
        return None
