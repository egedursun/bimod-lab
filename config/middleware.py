import re
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _, activate
from lxml import html
import logging

from config.settings import HTTP_ERROR_PATHS, SUFFIX_ANY, TRANSLATOR_DEBUG_MODE, ACTIVATE_MANUAL_TRANSLATION

logger = logging.getLogger(__name__)

HTTP_STATUS_QUERY_TAG = 'http_status'
HTTP_STATUS_ERROR_TAG_VALUE = 'error'


from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve, Resolver404

HTTP_STATUS_QUERY_TAG = "status"
HTTP_STATUS_ERROR_TAG_VALUE = "error"

class AppendStatusMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        This method ensures that URLs without a trailing slash are redirected correctly,
        and handles appending a status=error tag if the URL cannot be resolved.
        """
        path_info = request.path_info

        # First, ensure the URL ends with a slash
        if not path_info.endswith('/'):
            # Redirect to the URL with a trailing slash
            new_path_info = f"{path_info}/"
            parsed_url = urlparse(request.get_full_path())
            new_url = parsed_url._replace(path=new_path_info)
            return HttpResponsePermanentRedirect(urlunparse(new_url))

        # If the URL is already resolved with the error tag, try to resolve it
        if HTTP_STATUS_QUERY_TAG in request.GET:
            try:
                resolved = resolve(path_info)
                # If resolved and the error tag exists, remove only the error tag and redirect
                if resolved:
                    parsed_url = urlparse(request.get_full_path())
                    query_params = parse_qs(parsed_url.query)
                    if HTTP_STATUS_QUERY_TAG in query_params and HTTP_STATUS_ERROR_TAG_VALUE in query_params[HTTP_STATUS_QUERY_TAG]:
                        query_params[HTTP_STATUS_QUERY_TAG].remove(HTTP_STATUS_ERROR_TAG_VALUE)
                        # Clean up if the status tag becomes empty
                        if not query_params[HTTP_STATUS_QUERY_TAG]:
                            del query_params[HTTP_STATUS_QUERY_TAG]
                        new_query_string = urlencode(query_params, doseq=True)
                        new_url = urlunparse(parsed_url._replace(query=new_query_string))
                        return HttpResponsePermanentRedirect(new_url)
            except Resolver404:
                # If Resolver404 is raised, keep the error tag as it is
                pass  # Continue processing as the URL is not resolvable

        # If the URL is not resolved, add the error tag and redirect
        try:
            resolve(path_info)
        except Resolver404:
            if HTTP_STATUS_QUERY_TAG not in request.GET:
                parsed_url = urlparse(request.get_full_path())
                query_params = parse_qs(parsed_url.query)
                query_params[HTTP_STATUS_QUERY_TAG] = [HTTP_STATUS_ERROR_TAG_VALUE]
                new_query_string = urlencode(query_params, doseq=True)
                new_url = urlunparse(parsed_url._replace(query=new_query_string))
                return HttpResponsePermanentRedirect(new_url)

        return None  # Allow normal processing to continue


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


class ManualTranslationMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not ACTIVATE_MANUAL_TRANSLATION:
            return response
        # Check if the response is HTML
        if 'text/html' in response['Content-Type'].lower():
            try:
                # Activate Turkish language
                activate('tr')
                # Decode the response content
                charset = response.charset if response.charset else 'utf-8'
                try:
                    content = response.content.decode(charset)
                except Exception as e:
                    logger.error(f"Decoding error: {e}")
                    raise
                # Parse the HTML content
                try:
                    tree = html.fromstring(content)
                except Exception as e:
                    logger.error(f"HTML parsing error: {e}")
                    raise
                self.translate_text(tree)
                # Serialize the HTML content back to a string with UTF-8 encoding
                try:
                    response.content = html.tostring(tree, encoding='utf-8')
                except Exception as e:
                    logger.error(f"Serialization error: {e}")
                    raise
                # Update the content length header
                response['Content-Length'] = str(len(response.content))
                # Ensure the response charset is set to UTF-8
                response.charset = 'utf-8'
            except Exception as e:
                # Log the error and return the original response
                logger.error(f"Translation error: {e}")
        return response

    def translate_text(self, tree):
        """Translate text elements in the HTML tree."""

        def is_within_div(elem):
            """Check if the element is within a <div> tag."""
            while elem is not None:
                if isinstance(elem.tag, str) and elem.tag.lower() == 'div':
                    return True
                elem = elem.getparent()
            return False

        for elem in tree.iter():
            text_clean = re.sub(r'\s+', ' ', elem.text.strip()) if elem.text else ''
            tail_clean = re.sub(r'\s+', ' ', elem.tail.strip()) if elem.tail else ''
            if text_clean and text_clean.strip() and is_within_div(elem):
                elem.text = self.get_translation(text_clean)
            if tail_clean and tail_clean.strip() and is_within_div(elem):
                elem.tail = self.get_translation(tail_clean)

    def get_translation(self, text):
        """Get translation for the given text using Django's i18n."""
        translated_text = _(text if text else None)
        if translated_text and translated_text != text:
            if TRANSLATOR_DEBUG_MODE:
                print(f"Translated: | {text} | -----> | {translated_text} |")
            pass
        else:
            if TRANSLATOR_DEBUG_MODE:
                print(f"Unchanged: | {text} |")
            pass
        return translated_text if translated_text != text else text
