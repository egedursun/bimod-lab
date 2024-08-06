from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin

from config.settings import HTTP_ERROR_PATHS


class AppendStatusMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            # Try to resolve the URL, if it fails it will raise Resolver404
            resolve(request.path)
        except Resolver404:
            if 'status' not in request.GET:
                new_url = f"{request.path}?status=error"
                return HttpResponsePermanentRedirect(new_url)
        return None


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # if the page is among the excluded pages, return None
        for excluded_page in settings.EXCLUDED_PAGES:
            # Directly exclude exported assistants from authentication
            if excluded_page == "/app/exported_assistants/exported/":
                if request.path.startswith(excluded_page):
                    return None
            elif excluded_page in HTTP_ERROR_PATHS:
                query_params = request.GET
                status_code = query_params.get('status', "")
                if status_code == "error":
                    return None
            # Exclude other pages from authentication only if they are the exact page
            else:
                path_without_queries = request.path.split('?')[0] if '?' in request.path else request.path
                if path_without_queries == excluded_page:
                    return None
        if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
            return redirect(settings.LOGIN_URL)
        return None
