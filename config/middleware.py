from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin

from config.settings import HTTP_ERROR_PATHS, SUFFIX_ANY

HTTP_STATUS_QUERY_TAG = 'http_status'
HTTP_STATUS_ERROR_TAG_VALUE = 'error'


class AppendStatusMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            # Try to resolve the URL, if it fails it will raise Resolver404
            resolve(request.path)
        except Resolver404:
            if HTTP_STATUS_QUERY_TAG not in request.GET:
                new_url = f"{request.path}?{HTTP_STATUS_QUERY_TAG}={HTTP_STATUS_ERROR_TAG_VALUE}"
                return HttpResponsePermanentRedirect(new_url)
        return None


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # if the page is among the excluded pages, return None
        for excluded_page in settings.EXCLUDED_PAGES:
            # Directly exclude exported assistants from authentication
            if excluded_page in HTTP_ERROR_PATHS:
                query_params = request.GET
                status_code = query_params.get(HTTP_STATUS_QUERY_TAG, "")
                if status_code == HTTP_STATUS_ERROR_TAG_VALUE:
                    return None
            # Exclude other pages from authentication only if they are the exact page
            else:
                if SUFFIX_ANY in excluded_page:
                    if request.path.startswith(excluded_page.replace(SUFFIX_ANY, "")[:-1]):
                        return None
                else:
                    if request.path == excluded_page:
                        return None
        if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
            return redirect(settings.LOGIN_URL)
        return None
