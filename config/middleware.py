import re

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
