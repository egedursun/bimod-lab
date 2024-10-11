#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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


NUMBER_OF_RANDOM_FEATURED_SCRIPTS = 5

SCRIPT_SOURCES = {
    "internal": "internal", "external": "external",
}

CUSTOM_SCRIPT_CATEGORIES = [
    ("data", "Data"),
    ("aiml", "AI/ML"),
    ("media", "Media"),
    ("automation", "Automation"),
    ("apis", "APIs"),
    ("finance", "Finance"),
    ("commerce", "Commerce"),
    ("support", "Support"),
    ("social", "Social"),
    ("iot", "IoT"),
    ("health", "Health"),
    ("legal", "Legal"),
    ("education", "Education"),
    ("travel", "Travel"),
    ("security", "Security"),
    ("privacy", "Privacy"),
    ("entertainment", "Entertainment"),
    ("productivity", "Productivity"),
    ("utilities", "Utilities"),
    ("miscellaneous", "Miscellaneous"),
]

CUSTOM_SCRIPT_ADMIN_LIST = (
    "name",
    "is_public",
    "created_at",
    "updated_at",
)
CUSTOM_SCRIPT_ADMIN_SEARCH = (
    "name",
    "description",
)
CUSTOM_SCRIPT_ADMIN_LIST_FILTER = (
    "is_public",
)

CUSTOM_SCRIPT_REFERENCE_ADMIN_LIST = ("custom_script", "assistant", "created_by_user", "created_at", "updated_at")
CUSTOM_SCRIPT_REFERENCE_ADMIN_SEARCH = ("custom_script__name", "assistant__name")
CUSTOM_SCRIPT_REFERENCE_ADMIN_FILTER = ("assistant", "created_by_user")
