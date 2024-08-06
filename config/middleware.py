

from django.shortcuts import redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # if the page is among the excluded pages, return None
        for excluded_page in settings.EXCLUDED_PAGES:
            if request.path.startswith("/app/exported_assistants/exported/"):
                return None
            else:
                if request.path.startswith(excluded_page):
                    return None
        if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
            return redirect(settings.LOGIN_URL)
        return None
