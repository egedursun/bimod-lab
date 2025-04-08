"""
ASGI config for web_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import (
    AuthMiddlewareStack
)

from channels.routing import (
    URLRouter,
    ProtocolTypeRouter
)

from django.core.asgi import (
    get_asgi_application
)
from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.routing import Mount

from config.routing import (
    websocket_urlpatterns
)

from config.settings import BIMOD_REST_API_VERSION

from fastapi_server.utils import statuses

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django_app = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    }
)

######################
# API Server
######################

fastapi_app = FastAPI()

from fastapi.responses import JSONResponse


def check_api_key(request):
    api_key = request.headers.get("x-api-key")

    if api_key is None or api_key == "":
        return None, JSONResponse(
            {
                "status": statuses.ERROR,
                "message": "Invalid or missing API key in the request headers. Please provide the key within the 'x-api-key' header.",
                "errors": {
                    "api_key": "Missing API key"
                },
                "meta": {
                    "request": request.url.path,
                    "method": request.method,
                    "api_key": api_key
                }
            }
        )

    from auth.models import Profile

    associated_user = Profile.objects.filter(
        user_api_key=api_key,
    ).first()

    if associated_user is None:
        return None, JSONResponse(
            {
                "status": statuses.ERROR,
                "message": "Invalid API key in the request headers. Please provide the correct key.",
                "errors": {
                    "api_key": "No user found with the provided API key."
                },
                "meta": {
                    "request": request.url.path,
                    "method": request.method,
                    "api_key": api_key
                }
            }
        )

    return associated_user.user, None


from fastapi_server.services.setup import (
    router as router__quick_setup,
)

######################
# FastAPI Route Registrations
######################

# Commented out by @egedursun for stability increments.
# fastapi_app.include_router(router__assistants, prefix="/assistants")

fastapi_app.include_router(router__quick_setup, prefix="/setup")

######################

application = Starlette(routes=[
    Mount(f"/api/v{BIMOD_REST_API_VERSION}", app=fastapi_app),
    Mount("/", app=django_app),
])
