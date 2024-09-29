#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: constant_utils.py
#  Last Modified: 2024-09-28 16:08:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:59:56
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.


API_SOURCES = {
    "internal": "internal",
    "external": "external",
}
CUSTOM_API_CATEGORIES = [
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
