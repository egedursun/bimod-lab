#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: mtest_browsing.py
#  Last Modified: 2024-08-07 16:37:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:37:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml.html.clean import Cleaner


IMPLICIT_WAIT_SECONDS = 2


class SearchEnginesNames:
    GOOGLE = "google"
    YANDEX = "yandex"
    BING = "bing"
    DUCKDUCKGO = "duckduckgo"
    YAHOO = "yahoo"


class BrowserURLs:
    GOOGLE = "https://www.google.com"
    YANDEX = "https://www.yandex.com"
    BING = "https://www.bing.com"
    DUCKDUCKGO = "https://www.duckduckgo.com"
    YAHOO = "https://www.yahoo.com"


class FindByTypes:
    ID = By.ID; NAME = By.NAME; CSS_SELECTOR = By.CSS_SELECTOR
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME

    @staticmethod
    def as_list():
        return [
            FindByTypes.ID,
            FindByTypes.NAME,
            FindByTypes.CSS_SELECTOR,
            FindByTypes.XPATH,
            FindByTypes.LINK_TEXT,
            FindByTypes.PARTIAL_LINK_TEXT,
            FindByTypes.TAG_NAME,
            FindByTypes.CLASS_NAME
        ]


class ActionsNames:
    CONNECT = "connect"
    CLOSE = "close"
    BROWSER_SEARCH = "browser_search"
    CLICK_URL_IN_SEARCH = "click_url_in_search"

    @staticmethod
    def as_list():
        return [
            ActionsNames.CONNECT,
            ActionsNames.CLOSE,
            ActionsNames.BROWSER_SEARCH,
            ActionsNames.CLICK_URL_IN_SEARCH,
        ]


class TestBrowsingExecutor:

    class BrowsingModes:
        STANDARD = "standard"
        WHITELIST = "whitelist"
        BLACKLIST = "blacklist"

    def __init__(self, connection, headless=True):
        self.connection = connection
        # self.engine = connection.browser_type
        self.engine = SearchEnginesNames.DUCKDUCKGO
        self.d = None
        self.blacklisted_extensions = self.connection.blacklisted_extensions if self.connection else [

        ]
        self.whitelisted_extensions = self.connection.whitelisted_extensions if self.connection else [

        ]
        mode = self.BrowsingModes.STANDARD
        if self.whitelisted_extensions != [] or self.blacklisted_extensions != []:
            if self.whitelisted_extensions:
                mode = self.BrowsingModes.WHITELIST
            if self.blacklisted_extensions:
                mode = self.BrowsingModes.BLACKLIST
        self.mode = mode
        self.headless = headless

    ##################################################
    # AUTOMATOR
    ##################################################

    def act(self, action, **kwargs):
        if action == ActionsNames.CONNECT:
            return self.connect_c()
        elif action == ActionsNames.CLOSE:
            return self.close_c()
        elif action == ActionsNames.BROWSER_SEARCH:
            return self.browser_search(kwargs["search_query"], kwargs["page"])
        elif action == ActionsNames.CLICK_URL_IN_SEARCH:
            return self.click_url_in_search(kwargs["search_results"], kwargs["click_url"])
        else:
            return f"Invalid action: {action}. Must be one of {ActionsNames.as_list()}."

    ##################################################
    # VISIBLE METHODS
    ##################################################

    def connect_c(self):
        try:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('headless')
            d = webdriver.Chrome(options=options); self.d = d
            d.implicitly_wait(IMPLICIT_WAIT_SECONDS)
        except Exception as e:
            return f"There has been an unexpected error while trying to connect to the driver: {e}"

    def close_c(self):
        try: self.d.quit()
        except Exception as e:
            return f"There has been an unexpected error while trying to close the driver: {e}"

    ##################################################

    def browser_search(self, search_query, page=1):
        if self.engine == SearchEnginesNames.GOOGLE:
            self.get_page(BrowserURLs.GOOGLE)
        elif self.engine == SearchEnginesNames.DUCKDUCKGO:
            self.get_page(BrowserURLs.DUCKDUCKGO)
        elif self.engine == SearchEnginesNames.YANDEX:
            self.get_page(BrowserURLs.YANDEX)
        elif self.engine == SearchEnginesNames.BING:
            self.get_page(BrowserURLs.BING)
        elif self.engine == SearchEnginesNames.YAHOO:
            self.get_page(BrowserURLs.YAHOO)
        else: return f"Invalid search engine: {self.engine}."

        if self.engine == SearchEnginesNames.GOOGLE:
            search_input = self.find(FindByTypes.NAME, "q")
            self.send_keys(search_input, search_query)
            search_input.submit()
        elif self.engine == SearchEnginesNames.DUCKDUCKGO:
            # approach according to the HTML of the DuckDuckGo search page
            search_input = self.d.find_element(By.ID, "search_form_input_homepage")
            self.send_keys(search_input, search_query)
        elif self.engine == SearchEnginesNames.YANDEX:
            search_input = self.find(FindByTypes.ID, "text")
            self.send_keys(search_input, search_query)
            search_input.submit()
        elif self.engine == SearchEnginesNames.BING:
            search_input = self.find(FindByTypes.ID, "sb_form_q")
            self.send_keys(search_input, search_query)
            search_input.submit()
        elif self.engine == SearchEnginesNames.YAHOO:
            search_input = self.find(FindByTypes.ID, "uh-search-box")
            self.send_keys(search_input, search_query)
            search_input.submit()

        self.wait()
        # check the current page
        if page > 1:
            next_page = self.find(FindByTypes.CSS_SELECTOR, "a#pnnext"); self.click(next_page)
            self.wait()

        return self.get_search_results()

    def get_page(self, url):
        try:
            self.d.get(url)
        except Exception as e:
            return f"There has been an unexpected error while trying to get the url on browsing: {e}"

    def get_title(self):
        try: return self.d.title
        except Exception as e:
            return f"There has been an unexpected error while trying to get the title on browsing: {e}"

    def get_page_content(self):
        try:
            clean_content = self.clean_page_content(self.d.page_source)
            return clean_content
        except Exception as e: return (f"There has been an unexpected error while trying to get the content on "
                                       f"browsing: {e}")

    def get_search_results(self):
        try:
            raw_results = self.d.find_elements(By.CSS_SELECTOR, "div.g")
            clean_results = self.get_cleaned_search_results(raw_results)

            if self.mode == self.BrowsingModes.WHITELIST:
                clean_results = self.filter_on_whitelist(clean_results)
            elif self.mode == self.BrowsingModes.BLACKLIST:
                clean_results = self.filter_on_blacklist(clean_results)
            return clean_results
        except Exception as e:
            return (f"There has been an unexpected error while trying to get the search results "
                                       f"on browsing: {e}")

    def wait(self):
        try:
            time.sleep(IMPLICIT_WAIT_SECONDS)
        except Exception as e:
            return f"There has been an unexpected error while trying to wait on browsing: {e}"

    def find(self, by, query):
        try:
            if by not in FindByTypes.as_list():
                return f"Invalid 'by' type: {by}. Must be one of {FindByTypes.as_list()}."
            return self.d.find_element(by=by, value=query)
        except Exception as e: return (f"There has been an unexpected error while trying to find the element on "
                                       f"browsing: {e}")

    def send_keys(self, element, text):
        try:
            element.send_keys(text)
            element.submit()
        except Exception as e:
            return f"There has been an unexpected error while trying to send keys to the element on browsing: {e}"

    def click_url_in_search(self, search_results, click_url):
        try:
            for r in search_results:
                if r["url"] == click_url:
                    self.get_page(r["url"])
                    content = self.get_page_content()
                    return content
            return f"URL not found in search results: {click_url}"
        except Exception as e:
            return (f"There has been an unexpected error while trying to click the URL in the "
                                       f"search results on browsing: {e}")

    def click(self, element):
        try: element.click()
        except Exception as e: return f"There has been an unexpected error while trying to click the element on browsing: {e}"

    def filter_on_whitelist(self, res):
        filtered_results = []
        for r in res:
            r["url"] = r["url"].split("/")[2]
            for ext in self.whitelisted_extensions:
                if r["url"].endswith(ext):
                    filtered_results.append(r)
                    break
        return filtered_results

    def filter_on_blacklist(self, res):
        filtered_results = []
        for r in res:
            blacklisted = False
            # take the main domain
            r["url"] = r["url"].split("/")[2]
            for ext in self.blacklisted_extensions:
                if r["url"].endswith(ext):
                    blacklisted = True
                    break
            if not blacklisted: filtered_results.append(r)
        return filtered_results

    ##################################################
    # INVISIBLE METHODS
    ##################################################

    @staticmethod
    def get_cleaned_search_results(raw_selenium_results):
        cleaned_results = []
        for r in raw_selenium_results:
            clean = {}; url = r.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            title = r.find_element(By.CSS_SELECTOR, "h3").text; snippet = r.find_element(By.CSS_SELECTOR, "span").text
            clean["url"] = url; clean["title"] = title; clean["snippet"] = snippet; cleaned_results.append(clean)
        return cleaned_results

    @staticmethod
    def clean_page_content(text):
        # only get the textual contents of the page, along with the URLs, nothing else
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        cleaner.comments = True
        cleaner.links = True
        cleaner.meta = True
        cleaner.page_structure = False
        cleaner.processing_instructions = True
        cleaner.embedded = True
        cleaner.frames = True
        cleaner.forms = False
        cleaner.annoying_tags = True
        cleaner.allow_tags = ['']
        cleaner.remove_unknown_tags = False
        text = cleaner.clean_html(text)
        # remove the final html tag
        text = (text.replace("\n", "").replace("\t", ""))
        text = " ".join(text.split())
        return text

##################################################
# Test 1
##################################################

search_query = "funny articles"

# Create a connection
executor = TestBrowsingExecutor(connection=None)

# [1] Connect
executor.act(ActionsNames.CONNECT)

# [2] Search
results = executor.act(ActionsNames.BROWSER_SEARCH, search_query=search_query, page=1)

print("RESULTS: ")
pprint(results)

# [3] Click the first result
content = executor.act(ActionsNames.CLICK_URL_IN_SEARCH, search_results=results, click_url=results[0]["url"])

# [4] Close
executor.act(ActionsNames.CLOSE)


##################################################
# SEE THE RESULTS
##################################################
pprint(results[0]["url"])
pprint(content)

