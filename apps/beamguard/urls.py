#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-12-02 01:18:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:18:32
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

from apps.beamguard.views import (
    BeamGuardView_AbsolveArtifact,
    BeamGuardView_PurgeAllArtifacts,
    BeamGuardView_ListArtifacts,
    BeamGuardView_DiscardArtifact,
)

app_name = 'beamguard'

urlpatterns = [
    path(
        'artifacts/list/',
        BeamGuardView_ListArtifacts.as_view(
            template_name='beamguard/list_beamguard_artifacts.html'
        ),
        name='list'
    ),

    path(
        'artifacts/absolve/<int:pk>/',
        BeamGuardView_AbsolveArtifact.as_view(

        ),
        name='absolve'
    ),

    path(
        'artifacts/discard/<int:pk>/',
        BeamGuardView_DiscardArtifact.as_view(

        ),
        name='discard'
    ),

    path(
        'artifacts/purge/',
        BeamGuardView_PurgeAllArtifacts.as_view(

        ),
        name='purge'
    ),
]
