#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
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

BROWSER_TYPES = [
    ("google", "Google"),
]


class BrowserTypesNames:
    GOOGLE = "google"

    @staticmethod
    def as_list():
        return [BrowserTypesNames.GOOGLE]


BROWSER_READING_ABILITIES = [
    ("javascript", "JavaScript"),
    ("style", "Style"),
    ("inline_style", "Inline Style"),
    ("comments", "Comments"),
    ("links", "Links"),
    ("meta", "Meta"),
    ("page_structure", "Page Structure"),
    ("processing_instructions", "Processing Instructions"),
    ("embedded", "Embedded"),
    ("frames", "Frames"),
    ("forms", "Forms"),
    ("keep_tags", "Keep Tags"),
]


class BrowsingReadingAbilitiesNames:
    JAVASCRIPT = "javascript"
    STYLE = "style"
    INLINE_STYLE = "inline_style"
    COMMENTS = "comments"
    LINKS = "links"
    META = "meta"
    PAGE_STRUCTURE = "page_structure"
    PROCESSING_INSTRUCTIONS = "processing_instructions"
    EMBEDDED = "embedded"
    FRAMES = "frames"
    FORMS = "forms"
    REMOVE_TAGS = "remove_tags"


BROWSER_ADMIN_LIST = [
    'assistant',
    'browser_type',
    'name',
    'data_selectivity',
    'created_at',
    'updated_at'
]
BROWSER_ADMIN_SEARCH = [
    'assistant',
    'name',
    'description',
    'created_at',
    'updated_at'
]
BROWSER_ADMIN_FILTER = [
    'assistant',
    'browser_type',
    'data_selectivity'
]

BROWSING_LOG_ADMIN_LIST = [
    'id',
    'connection',
    'action',
    'created_at'
]
BROWSING_LOG_ADMIN_SEARCH = [
    'connection',
    'action',
    'html_content',
    'log_content',
    'created_at'
]
BROWSING_LOG_ADMIN_FILTER = [
    'connection',
    'action',
    'created_at'
]
