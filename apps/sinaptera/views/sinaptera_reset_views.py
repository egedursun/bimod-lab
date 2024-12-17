#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sinaptera_reset_views.py
#  Last Modified: 2024-12-16 23:13:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-16 23:13:28
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

from django.views import View

from apps.sinaptera.models import (
    SinapteraConfiguration
)

logger = logging.getLogger(__name__)


class SinapteraView_ResetConfiguration(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(
            request=request,
            *args,
            **kwargs
        )

    def post(self, request, *args, **kwargs):

        user = request.user

        try:
            SinapteraConfiguration.objects.get(
                user=user
            ).delete()

        except Exception as e:
            messages.error(
                request,
                'An error occurred while resetting the Sinaptera configuration.'
            )

            logger.error(
                f'An error occurred while resetting the Sinaptera configuration: {e}'
            )

            return redirect('sinaptera:configuration')

        # Create a new Sinaptera configuration

        try:
            new_configuration = SinapteraConfiguration.objects.create(
                user=user
            )

            new_configuration.save()

            messages.success(
                request,
                'Sinaptera configuration has been successfully reset.'
            )

        except Exception as e:
            messages.error(
                request,
                'An error occurred while resetting the Sinaptera configuration.'
            )

            logger.error(
                f'An error occurred while resetting the Sinaptera configuration: {e}'
            )

            return redirect('sinaptera:configuration')

        return redirect('sinaptera:configuration')
