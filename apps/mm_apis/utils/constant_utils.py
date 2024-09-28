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
