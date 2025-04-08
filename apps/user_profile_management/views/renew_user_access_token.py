#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: renew_user_access_token.py
#  Last Modified: 2025-02-01 12:00:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-01 12:00:58
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
import secrets

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.views import View

from apps.metatempo.utils import (
    USER_API_KEY_DEFAULT_LENGTH
)

logger = logging.getLogger(__name__)


class UserProfileView_ResetAPIKey(LoginRequiredMixin, View):
    def get(
        self,
        request,
        *args,
        **kwargs
    ):
        return self.post(
            request,
            *args,
            **kwargs
        )

    def post(
        self,
        request,
        *args,
        **kwargs
    ):
        context_user: User = request.user

        new_api_key = secrets.token_urlsafe(
            USER_API_KEY_DEFAULT_LENGTH
        )

        context_user.profile.user_api_key = new_api_key
        context_user.profile.save()

        logger.info(f"User {context_user.username} has renewed their API key.")

        return redirect('user_profile_management:list')
