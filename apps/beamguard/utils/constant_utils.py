#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-12-02 01:19:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:19:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

BEAMGUARD_ARTIFACT_TYPES = [
    ("sql", "SQL"),
    ("nosql", "NoSQL"),
    ("file_system", "File System"),
]


BEAMGUARD_CONFIRMATION_STATUSES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("rejected", "Rejected"),
]


class BeamGuardConfirmationStatusesNames:
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'

    @staticmethod
    def as_list():
        return [
            BeamGuardConfirmationStatusesNames.PENDING,
            BeamGuardConfirmationStatusesNames.CONFIRMED,
            BeamGuardConfirmationStatusesNames.REJECTED,
        ]


class BeamGuardArtifactTypesNames:
    SQL = 'sql'
    NOSQL = 'nosql'
    FILE_SYSTEM = 'file_system'

    @staticmethod
    def as_list():
        return [
            BeamGuardArtifactTypesNames.SQL,
            BeamGuardArtifactTypesNames.NOSQL,
            BeamGuardArtifactTypesNames.FILE_SYSTEM,
        ]


BEAMGUARD_ARTIFACT_ADMIN_LIST = (
    'assistant',
    'type',
    'created_at'
)
BEAMGUARD_ARTIFACT_ADMIN_SEARCH = (
    'assistant__name',
    'type',
    'created_at'
)
BEAMGUARD_ARTIFACT_ADMIN_FILTER = (
    'assistant',
    'type',
    'created_at'
)


class BeamGuardLogReceiverTypesNames:
    ASSISTANT = "assistant"
    LEANMOD = "leanmod"
    VOIDFORGER = "voidforger"

    @staticmethod
    def as_list():
        return [
            BeamGuardLogReceiverTypesNames.ASSISTANT,
            BeamGuardLogReceiverTypesNames.LEANMOD,
            BeamGuardLogReceiverTypesNames.VOIDFORGER
        ]
