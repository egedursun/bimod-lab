class StatusCodes:
    """
    A simple class containing HTTP status codes used throughout the views.

    Attributes:
        OK (int): HTTP 200 OK.
        NOT_FOUND (int): HTTP 404 Not Found.
        UNAUTHORIZED (int): HTTP 401 Unauthorized.
        TOO_MANY_REQUESTS (int): HTTP 429 Too Many Requests.
        SERVICE_OFFLINE (int): HTTP 503 Service Unavailable.
        INTERNAL_SERVER_ERROR (int): HTTP 500 Internal Server Error.
    """
    OK = 200
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    TOO_MANY_REQUESTS = 429
    SERVICE_OFFLINE = 503
    INTERNAL_SERVER_ERROR = 500
