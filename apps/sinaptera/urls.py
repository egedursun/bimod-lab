#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-12-14 17:07:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 17:07:02
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from apps.sinaptera.views import (
    SinapteraView_Configuration,
    SinapteraView_ResetConfiguration
)

app_name = 'sinaptera'

urlpatterns = [
    path(
        'configuration/',
        SinapteraView_Configuration.as_view(
            template_name='sinaptera/sinaptera_configuration.html'
        ),
        name='configuration'
    ),

    path(
        'reset-configuration/',
        SinapteraView_ResetConfiguration.as_view(),
        name='reset_configuration'
    ),
]
