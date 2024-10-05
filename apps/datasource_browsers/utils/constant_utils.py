#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

BROWSER_TYPES = [
    ("google", "Google"),
]

BROWSER_READING_ABILITIES = [
    # Remove these contents
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
