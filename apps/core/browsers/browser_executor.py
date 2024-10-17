#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: browser_executor.py
#  Last Modified: 2024-10-05 02:13:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import base64
import logging
import time
import uuid

from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml.html.clean import Cleaner

from apps.core.browsers.utils import IMPLICIT_WAIT_SECONDS, SearchEnginesNames, BrowserURLs, FindByTypes, \
    BrowserActionsNames, BrowsingModes, BrowsingExecutorOptions
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.datasource_browsers.utils import BrowsingReadingAbilitiesNames
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


logger = logging.getLogger(__name__)


class BrowsingExecutor:
    def __init__(self, connection):
        self.connection = connection
        self.engine = connection.browser_type
        self.d = None
        self.blacklisted_extensions = self.connection.blacklisted_extensions if self.connection else []
        self.whitelisted_extensions = self.connection.whitelisted_extensions if self.connection else []
        try:
            mode = BrowsingModes.STANDARD
            if self.whitelisted_extensions != [] or self.blacklisted_extensions != []:
                if self.whitelisted_extensions:
                    mode = BrowsingModes.WHITELIST
                if self.blacklisted_extensions:
                    mode = BrowsingModes.BLACKLIST
        except Exception as e:
            mode = BrowsingModes.STANDARD
            logger.error(f"Error while setting browsing mode, setting to standard: {str(e)}")
        try:
            self.mode = mode
            self.connect_c()
            logger.info(f"Connected to the browsing driver.")
        except Exception as e:
            logger.error(f"Error while connecting to the browsing driver: {str(e)}")
            pass


    def act(self, action, **kwargs):
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        try:
            tx = LLMTransaction(
                organization=self.connection.assistant.organization, model=self.connection.assistant.llm_model,
                responsible_user=None, responsible_assistant=self.connection.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.BrowsingExecutor.COST,
                transaction_type=ChatRoles.SYSTEM, transaction_source=LLMTransactionSourcesTypesNames.BROWSING,
                is_tool_cost=True)
            tx.save()
            logger.info(f"LLM Transaction created for browsing action: {action}.")
        except Exception as e:
            logger.error(f"Error while creating LLM Transaction for browsing action: {str(e)}")
            pass

        if action == BrowserActionsNames.BROWSER_SEARCH:
            try:
                search_output, image_bytes = self.browser_search(kwargs["query"], kwargs["page"])
                logger.info(f"Search query: {kwargs['query']} for the {kwargs['page']}th page of the {self.engine}"
                            f"search engine.")
            except Exception as e:
                logger.error(f"Error while searching the query: {str(e)}")
                return None

            try:
                new_log_instance = self.connection.logs.create(
                    connection=self.connection, action=action, context_url=None, html_content=None,
                    context_content=search_output,
                    log_content=f"Search query: {kwargs['query']} for the {kwargs['page']}th page of the {self.engine}"
                                f"search engine.",
                    screenshot=ContentFile(image_bytes, name=f"{uuid.uuid4()}.png")
                )
                new_log_instance.save()
                logger.info(f"Log instance created for the search query: {kwargs['query']} for the {kwargs['page']}th"
                            f"page of the {self.engine} search engine.")
            except Exception as e:
                logger.error(f"Error while creating log instance for the search query: {str(e)}")
                pass
            return search_output
        elif action == BrowserActionsNames.CLICK_URL_IN_SEARCH:
            try:
                click_response, image_bytes = self.click_url_in_search(kwargs["search_results"], kwargs["click_url"])
                logger.info(f"Clicked the URL: {kwargs['click_url']} in the search results.")
            except Exception as e:
                logger.error(f"Error while clicking the URL in the search results: {str(e)}")
                return None

            try:
                new_log_instance = self.connection.logs.create(
                    connection=self.connection, action=action, context_url=kwargs["click_url"],
                    html_content=click_response, context_content=None,
                    log_content=f"Clicked the URL: {kwargs['click_url']} in the search results.",
                    screenshot=ContentFile(image_bytes, name=f"{uuid.uuid4()}.png")
                )
                new_log_instance.save()
                logger.info(f"Log instance created for clicking the URL: {kwargs['click_url']} in the search results.")
            except Exception as e:
                logger.error(f"Error while creating log instance for clicking the URL in the search results: {str(e)}")
                pass
            return click_response
        else:
            logger.error(f"Invalid action: {action}. Must be one of {BrowserActionsNames.as_list()}.")
            return f"[BrowsingExecutor.act] Invalid action: {action}. Must be one of {BrowserActionsNames.as_list()}."

    def connect_c(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument(BrowsingExecutorOptions.HEADLESS)
            options.add_argument(BrowsingExecutorOptions.WINDOW_SIZE)
            d = webdriver.Chrome(options=options)
            self.d = d
            logger.info(f"Connected to the browsing driver.")
        except Exception as e:
            logger.error(f"Error while connecting to the browsing driver: {str(e)}")
            return (f"[BrowsingExecutor.connect_c] There has been an unexpected error while trying to "
                    f"connect to the driver: {e}")

    def close_c(self):
        try:
            self.d.quit()
            logger.info(f"Closed the browsing driver.")
        except Exception as e:
            logger.error(f"Error while closing the browsing driver: {str(e)}")
            return (f"[BrowsingExecutor.close_c] There has been an unexpected error while trying to close the "
                    f"driver: {e}")

    def browser_search(self, query, page=1):
        if self.engine == SearchEnginesNames.GOOGLE:
            self.get_page(BrowserURLs.GOOGLE)
        else:
            logger.error(f"Invalid search engine: {self.engine}.")
            return f"[BrowsingExecutor.browser_search] Invalid search engine: {self.engine}."
        search_input = self.find(FindByTypes.NAME, "q")
        try:
            self.send_keys(search_input, query)
            search_input.submit()
            self.wait()
            logger.info(f"Search query: {query} for the {page}th page of the {self.engine} search engine.")
        except Exception as e:
            logger.error(f"Error while searching the query: {str(e)}")
            return (f"[BrowsingExecutor.browser_search] There has been an unexpected error while trying to search "
                    f"the query: {e}")

        if page > 1:
            try:
                next_page = self.find(FindByTypes.CSS_SELECTOR, "a#pnnext")
                self.click(next_page)
                self.wait()
                logger.info(f"Going to the next page for the search query: {query} for the {page}th page of the "
                            f"{self.engine} search engine.")
            except Exception as e:
                logger.error(f"Error while going to the next page: {str(e)}")
                return (f"[BrowsingExecutor.browser_search] There has been an unexpected error while trying to "
                        f"go to the next page: {e}")
        return self.get_search_results()

    def get_page(self, url):
        try:
            self.d.get(url)
            logger.info(f"Opened the URL: {url} on browsing driver.")
        except Exception as e:
            logger.error(f"Error while opening the URL: {str(e)}")
            return (f"[BrowsingExecutor.get_page] There has been an unexpected error while trying to get the url on "
                    f"browsing: {e}")

    def get_title(self):
        try:
            logger.info(f"Getting the title of the page.")
            return self.d.title
        except Exception as e:
            logger.error(f"Error while getting the title: {str(e)}")
            return (f"[BrowsingExecutor.get_title] There has been an unexpected error while trying to get the title "
                    f"on browsing: {e}")

    def get_page_content(self):
        try:
            clean_content = self.clean_page_content(self.d.page_source)
            logger.info(f"Getting the content of the page.")
            return clean_content
        except Exception as e:
            logger.error(f"Error while getting the content: {str(e)}")
            return (
                f"[BrowsingExecutor.get_page_content] There has been an unexpected error while trying to get the "
                f"content on browsing: {e}")

    def get_search_results(self):
        try:
            image_b64 = self.d.get_screenshot_as_base64()
            image_bytes = base64.b64decode(image_b64)
            logger.info(f"Getting the search results.")
        except Exception as e:
            logger.error(f"Error while getting the screenshot: {str(e)}")
            return (
                f"[BrowsingExecutor.get_search_results] There has been an unexpected error while trying to get the "
                f"screenshot on browsing: {e}")
        try:
            raw_results = self.d.find_elements(By.CSS_SELECTOR, "div.g")
            clean_results = self.get_cleaned_search_results(raw_results)
            if self.mode == BrowsingModes.WHITELIST:
                clean_results = self.filter_on_whitelist(clean_results)
            elif self.mode == BrowsingModes.BLACKLIST:
                clean_results = self.filter_on_blacklist(clean_results)
            logger.info(f"Search results: {clean_results}")
            return clean_results, image_bytes
        except Exception as e:
            logger.error(f"Error while getting the search results: {str(e)}")
            return (
                f"[BrowsingExecutor.get_search_results] There has been an unexpected error while trying to get the "
                f"search results on browsing: {e}")

    def wait(self):
        try:
            time.sleep(IMPLICIT_WAIT_SECONDS)
            logger.info(f"Waiting on browsing.")
        except Exception as e:
            logger.error(f"Error while waiting: {str(e)}")
            return f"[[BrowsingExecutor.wait] There has been an unexpected error while trying to wait on browsing: {e}"

    def find(self, by, query):
        try:
            if by not in FindByTypes.as_list():
                return f"[BrowsingExecutor.find] Invalid 'by' type: {by}. Must be one of {FindByTypes.as_list()}."
            logger.info(f"Finding the element on browsing.")
            return self.d.find_element(by=by, value=query)
        except Exception as e:
            logger.error(f"Error while finding the element: {str(e)}")
            return (
                f"[BrowsingExecutor.find] There has been an unexpected error while trying to find the element on "
                f"browsing: {e}")

    def send_keys(self, element, text):
        try:
            element.send_keys(text)
            logger.info(f"Sending keys to the element on browsing.")
        except Exception as e:
            logger.error(f"Error while sending keys: {str(e)}")
            return (f"[BrowsingExecutor.send_keys] There has been an unexpected error while trying to send keys to the"
                    f" element on browsing: {e}")

    def click_url_in_search(self, search_results, click_url):
        try:
            for r in search_results:
                if r["url"] == click_url:
                    self.get_page(r["url"])
                    image_b64 = self.d.get_screenshot_as_base64()
                    image_bytes = base64.b64decode(image_b64)
                    content = self.get_page_content()
                    logger.info(f"Clicked the URL: {click_url} in the search results.")
                    return content, image_bytes
            return f"[BrowsingExecutor.click_url_in_search] URL not found in search results: {click_url}"
        except Exception as e:
            logger.error(f"Error while clicking the URL in the search results: {str(e)}")
            return (
                f"[BrowsingExecutor.click_url_in_search] There has been an unexpected error while trying to "
                f"click the URL in the search results on browsing: {e}")

    def click(self, element):
        try:
            element.click()
            logger.info(f"Clicked the element on browsing.")
        except Exception as e:
            logger.error(f"Error while clicking: {str(e)}")
            return (f"[BrowsingExecutor.click] There has been an unexpected error while trying to click "
                    f"the element on browsing: {e}")

    def filter_on_whitelist(self, res):
        filtered_results = []
        for r in res:
            try:
                r["url"] = r["url"].split("/")[2]
                for ext in self.whitelisted_extensions:
                    if r["url"].endswith(ext):
                        filtered_results.append(r)
                        break
            except Exception as e:
                logger.error(f"Error while filtering on whitelist: {str(e)}")
                pass
        logger.info(f"Filtered results on whitelist: {filtered_results}")
        return filtered_results

    def filter_on_blacklist(self, res):
        filtered_results = []
        for r in res:
            try:
                blacklisted = False
                r["url"] = r["url"].split("/")[2]
                for ext in self.blacklisted_extensions:
                    if r["url"].endswith(ext):
                        blacklisted = True
                        break
                if not blacklisted:
                    filtered_results.append(r)
            except Exception as e:
                logger.error(f"Error while filtering on blacklist: {str(e)}")
                pass
        logger.info(f"Filtered results on blacklist: {filtered_results}")
        return filtered_results

    @staticmethod
    def get_cleaned_search_results(raw_selenium_results):
        cleaned_results = []
        for r in raw_selenium_results:
            try:
                clean = {}
                url = r.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                title = r.find_element(By.CSS_SELECTOR, "h3").text
                snippet = r.find_element(By.CSS_SELECTOR, "span").text
                clean["url"] = url
                clean["title"] = title
                clean["snippet"] = snippet
                cleaned_results.append(clean)
            except Exception as e:
                logger.error(f"Error while cleaning the search results: {str(e)}")
                pass
        logger.info(f"Cleaned search results: {cleaned_results}")
        return cleaned_results

    def clean_page_content(self, text):
        abilities = self.connection.reading_abilities
        cleaner = Cleaner()
        cleaner.javascript = abilities[BrowsingReadingAbilitiesNames.JAVASCRIPT]
        cleaner.style = abilities[BrowsingReadingAbilitiesNames.STYLE]
        cleaner.comments = abilities[BrowsingReadingAbilitiesNames.COMMENTS]
        cleaner.links = abilities[BrowsingReadingAbilitiesNames.LINKS]
        cleaner.meta = abilities[BrowsingReadingAbilitiesNames.META]
        cleaner.page_structure = abilities[BrowsingReadingAbilitiesNames.PAGE_STRUCTURE]
        cleaner.processing_instructions = abilities[BrowsingReadingAbilitiesNames.PROCESSING_INSTRUCTIONS]
        cleaner.embedded = abilities[BrowsingReadingAbilitiesNames.EMBEDDED]
        cleaner.frames = abilities[BrowsingReadingAbilitiesNames.FRAMES]
        cleaner.forms = abilities[BrowsingReadingAbilitiesNames.FORMS]
        cleaner.annoying_tags = True
        if abilities[BrowsingReadingAbilitiesNames.REMOVE_TAGS]:
            cleaner.allow_tags = ['']
            cleaner.remove_unknown_tags = False

        try:
            text = cleaner.clean_html(text)
            text = (text.replace("<div>", "").replace("</div>", "").replace("\n", "")
                    .replace("\t", ""))
            text = " ".join(text.split())
            logger.info(f"Cleaned the page content.")
        except Exception as e:
            logger.error(f"Error while cleaning the page content: {str(e)}")
            return None
        return text
