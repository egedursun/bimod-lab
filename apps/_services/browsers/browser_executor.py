import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml.html.clean import Cleaner

from apps._services.config.costs_map import ToolCostsMap
from apps.datasource_browsers.models import BrowsingReadingAbilitiesNames, DataSourceBrowserBrowsingLog
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames

IMPLICIT_WAIT_SECONDS = 2


class SearchEnginesNames:
    GOOGLE = "google"


class BrowserURLs:
    GOOGLE = "https://www.google.com"


class FindByTypes:
    ID = By.ID
    NAME = By.NAME
    CSS_SELECTOR = By.CSS_SELECTOR
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME

    @staticmethod
    def as_list():
        return [FindByTypes.ID, FindByTypes.NAME, FindByTypes.CSS_SELECTOR, FindByTypes.XPATH, FindByTypes.LINK_TEXT,
                FindByTypes.PARTIAL_LINK_TEXT, FindByTypes.TAG_NAME, FindByTypes.CLASS_NAME]


class ActionsNames:
    BROWSER_SEARCH = "browser_search"
    CLICK_URL_IN_SEARCH = "click_url_in_search"

    @staticmethod
    def as_list():
        return [ActionsNames.BROWSER_SEARCH, ActionsNames.CLICK_URL_IN_SEARCH]


class BrowsingExecutor:
    class BrowsingModes:
        STANDARD = "standard"
        WHITELIST = "whitelist"
        BLACKLIST = "blacklist"

    def __init__(self, connection):
        self.connection = connection
        self.engine = connection.browser_type
        self.d = None
        self.blacklisted_extensions = self.connection.blacklisted_extensions if self.connection else []
        self.whitelisted_extensions = self.connection.whitelisted_extensions if self.connection else []
        mode = self.BrowsingModes.STANDARD
        if self.whitelisted_extensions != [] or self.blacklisted_extensions != []:
            if self.whitelisted_extensions:
                mode = self.BrowsingModes.WHITELIST
            if self.blacklisted_extensions:
                mode = self.BrowsingModes.BLACKLIST
        self.mode = mode
        self.connect_c()

    ##################################################
    # AUTOMATOR
    ##################################################

    def act(self, action, **kwargs):

        transaction = LLMTransaction(
            organization=self.connection.assistant.organization,
            model=self.connection.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection.assistant,
            encoding_engine="cl100k_base",
            llm_cost=ToolCostsMap.BrowsingExecutor.COST,
            transaction_type="system",
            transaction_source=TransactionSourcesNames.BROWSING,
            is_tool_cost=True
        )
        transaction.save()

        if action == ActionsNames.BROWSER_SEARCH:
            search_response =  self.browser_search(kwargs["query"], kwargs["page"])

            new_log_instance = self.connection.logs.create(
                connection=self.connection,
                action=action,
                context_url=None,
                html_content=None,
                context_content=search_response,
                log_content=f"Search query: {kwargs['query']} for the {kwargs['page']}th page of the {self.engine} "
                            f"search engine.",
            )
            new_log_instance.save()
            return search_response
        elif action == ActionsNames.CLICK_URL_IN_SEARCH:
            click_response = self.click_url_in_search(kwargs["search_results"], kwargs["click_url"])

            new_log_instance = self.connection.logs.create(
                connection=self.connection,
                action=action,
                context_url=kwargs["click_url"],
                html_content=click_response,
                context_content=None,
                log_content=f"Clicked the URL: {kwargs['click_url']} in the search results.",
            )
            new_log_instance.save()
            return click_response
        else:
            return f"Invalid action: {action}. Must be one of {ActionsNames.as_list()}."

    ##################################################
    # VISIBLE METHODS
    ##################################################

    def connect_c(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            d = webdriver.Chrome(options=options)
            self.d = d
        except Exception as e:
            return f"There has been an unexpected error while trying to connect to the driver: {e}"

    def close_c(self):
        try:
            self.d.quit()
        except Exception as e:
            return f"There has been an unexpected error while trying to close the driver: {e}"

    ##################################################

    def browser_search(self, query, page=1):
        if self.engine == SearchEnginesNames.GOOGLE:
            self.get_page(BrowserURLs.GOOGLE)
        else:
            return f"Invalid search engine: {self.engine}."
        search_input = self.find(FindByTypes.NAME, "q")
        self.send_keys(search_input, query)
        search_input.submit()
        self.wait()
        # check the next page if needed
        if page > 1:
            next_page = self.find(FindByTypes.CSS_SELECTOR, "a#pnnext")
            self.click(next_page)
            self.wait()

        return self.get_search_results()

    def get_page(self, url):
        try:
            self.d.get(url)
        except Exception as e:
            return f"There has been an unexpected error while trying to get the url on browsing: {e}"

    def get_title(self):
        try:
            return self.d.title
        except Exception as e:
            return f"There has been an unexpected error while trying to get the title on browsing: {e}"

    def get_page_content(self):
        try:
            clean_content = self.clean_page_content(self.d.page_source)
            return clean_content
        except Exception as e:
            return (f"There has been an unexpected error while trying to get the content on "
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
        except Exception as e:
            return (f"There has been an unexpected error while trying to find the element on "
                    f"browsing: {e}")

    def send_keys(self, element, text):
        try:
            element.send_keys(text)
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
        try:
            element.click()
        except Exception as e:
            return f"There has been an unexpected error while trying to click the element on browsing: {e}"

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
            clean = {}
            url = r.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            title = r.find_element(By.CSS_SELECTOR, "h3").text
            snippet = r.find_element(By.CSS_SELECTOR, "span").text
            clean["url"] = url
            clean["title"] = title
            clean["snippet"] = snippet
            cleaned_results.append(clean)
        return cleaned_results

    def clean_page_content(self, text):
        abilities = self.connection.reading_abilities

        # only get the textual contents of the page, along with the URLs, nothing else
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

        text = cleaner.clean_html(text)
        # remove the final html tag
        text = (text.replace("<div>", "").replace("</div>", "").replace("\n", "")
                .replace("\t", ""))
        text = " ".join(text.split())
        pprint(text)
        return text


##################################################
# Sample Usage
##################################################

"""
search_query = "resmi gazete yayınları"

# Create a connection
executor = BrowsingExecutor(connection=None)

# [1] Connect
executor.act(ActionsNames.CONNECT)

# [2] Search
results = executor.act(ActionsNames.BROWSER_SEARCH, search_query=search_query, page=2)

# [3] Click the first result
executor.act(ActionsNames.CLICK_URL_IN_SEARCH, search_results=results, click_url=results[0]["url"])

# [4] Close
executor.act(ActionsNames.CLOSE)
"""
