#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-30 17:42:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:42:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


ELLMA_SCRIPT_ADMIN_LIST = ['script_name', 'organization', 'llm_model', 'created_at', 'updated_at']
ELLMA_SCRIPT_ADMIN_SEARCH = ['script_name', 'organization__name', 'llm_model__nickname', 'created_by_user__email']
ELLMA_SCRIPT_ADMIN_FILTER = ['organization', 'llm_model', 'created_at', 'updated_at']

ELLMA_TRANSCRIPTION_LANGUAGES = [
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('typescript', 'TypeScript'),
    ('java', 'Java'),
    ('csharp', 'C#'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('go', 'Go'),
    ('rust', 'Rust'),
    ('ruby', 'Ruby'),
    ('php', 'PHP'),
    ('swift', 'Swift'),
    ('kotlin', 'Kotlin'),
    ('scala', 'Scala'),
    ('r', 'R'),
    ('perl', 'Perl'),
    ('bash', 'Bash'),
    ('powershell', 'PowerShell'),
]


class EllmaTranscriptionLanguagesNames:
    PYTHON3 = 'python3'
    JAVASCRIPT = 'javascript'
    TYPESCRIPT = 'typescript'
    JAVA = 'java'
    CSHARP = 'csharp'
    C = 'c'
    CPP = 'cpp'
    GO = 'go'
    RUST = 'rust'
    RUBY = 'ruby'
    PHP = 'php'
    SWIFT = 'swift'
    KOTLIN = 'kotlin'
    SCALA = 'scala'
    R = 'r'
    PERL = 'perl'
    BASH = 'bash'
    POWERSHELL = 'powershell'

    @staticmethod
    def as_list():
        return [
            EllmaTranscriptionLanguagesNames.PYTHON3,
            EllmaTranscriptionLanguagesNames.JAVASCRIPT,
            EllmaTranscriptionLanguagesNames.TYPESCRIPT,
            EllmaTranscriptionLanguagesNames.JAVA,
            EllmaTranscriptionLanguagesNames.CSHARP,
            EllmaTranscriptionLanguagesNames.C,
            EllmaTranscriptionLanguagesNames.CPP,
            EllmaTranscriptionLanguagesNames.GO,
            EllmaTranscriptionLanguagesNames.RUST,
            EllmaTranscriptionLanguagesNames.RUBY,
            EllmaTranscriptionLanguagesNames.PHP,
            EllmaTranscriptionLanguagesNames.SWIFT,
            EllmaTranscriptionLanguagesNames.KOTLIN,
            EllmaTranscriptionLanguagesNames.SCALA,
            EllmaTranscriptionLanguagesNames.R,
            EllmaTranscriptionLanguagesNames.PERL,
            EllmaTranscriptionLanguagesNames.BASH,
            EllmaTranscriptionLanguagesNames.POWERSHELL,
        ]
