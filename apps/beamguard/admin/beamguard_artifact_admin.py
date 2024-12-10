#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: beamguard_artifact_admin.py
#  Last Modified: 2024-12-02 01:23:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:23:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.beamguard.models import BeamGuardArtifact

from apps.beamguard.utils import (
    BEAMGUARD_ARTIFACT_ADMIN_LIST,
    BEAMGUARD_ARTIFACT_ADMIN_SEARCH,
    BEAMGUARD_ARTIFACT_ADMIN_FILTER,
)


@admin.register(BeamGuardArtifact)
class BeamGuardArtifactAdmin(admin.ModelAdmin):
    list_display = BEAMGUARD_ARTIFACT_ADMIN_LIST
    search_fields = BEAMGUARD_ARTIFACT_ADMIN_SEARCH
    list_filter = BEAMGUARD_ARTIFACT_ADMIN_FILTER

    ordering = ('-created_at',)
