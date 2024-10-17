#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


SOURCES_OF_CUSTOM_APIS = {
    "internal": "internal",
    "external": "external",
}

CATEGORIES_OF_CUSTOM_APIS = [
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

CUSTOM_API_AUTHENTICATION_TYPES = [
    ("None", "None"),
    ("Bearer", "Bearer")
]


class AcceptedHTTPRequestMethods:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


MAXIMUM_RETRIES = 3
NUMBER_OF_RANDOM_FEATURED_APIS = 5

CUSTOM_API_ADMIN_LIST = [
    "name",
    "created_by_user",
    "created_at",
    "updated_at",
]
CUSTOM_API_ADMIN_FILTER = ["categories", "created_at", "updated_at"]
CUSTOM_API_ADMIN_SEARCH = ["name", "description", "categories", "created_by_user__username"]

CUSTOM_API_REF_ADMIN_LIST = [
    "custom_api",
    "assistant",
    "api_source",
    "created_by_user",
    "created_at",
    "updated_at",
]
CUSTOM_API_REF_ADMIN_FILTER = ["api_source", "created_at", "updated_at"]
CUSTOM_API_REF_ADMIN_SEARCH = ["custom_api__name", "assistant__name", "api_source", "created_by_user__username"]
