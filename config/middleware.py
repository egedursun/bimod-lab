import re

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _, activate
from lxml import html
import logging

from config.settings import SUFFIX_ANY, TRANSLATOR_DEBUG_MODE, ACTIVATE_MANUAL_TRANSLATION

logger = logging.getLogger(__name__)

HTTP_STATUS_QUERY_TAG = 'http_status'
HTTP_STATUS_ERROR_TAG_VALUE = 'error'


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip authentication check for excluded pages
        for excluded_page in settings.EXCLUDED_PAGES:
            if SUFFIX_ANY in excluded_page:
                if request.path.startswith(excluded_page.replace(SUFFIX_ANY, "")[:-1]):
                    return None
            else:
                if request.path == excluded_page:
                    return None

        # If the user is not authenticated and the page is not the login page, redirect to login
        if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
            return redirect(settings.LOGIN_URL)
        return None


class AppendSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.endswith('/') and not request.path.startswith('/api/'):
            return HttpResponsePermanentRedirect(request.path + '/')
        return self.get_response(request)
