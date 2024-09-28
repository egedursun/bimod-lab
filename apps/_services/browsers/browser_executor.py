import base64
import time
import uuid

from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml.html.clean import Cleaner

from apps._services.browsers.utils import IMPLICIT_WAIT_SECONDS, SearchEnginesNames, BrowserURLs, FindByTypes, \
    BrowserActionsNames
from apps._services.config.costs_map import ToolCostsMap
from apps.datasource_browsers.utils import BrowsingReadingAbilitiesNames
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames


class BrowsingExecutor:
    class BrowsingModes:
        STANDARD = "standard"
        WHITELIST = "whitelist"
        BLACKLIST = "blacklist"

    class BrowsingExecutorOptions:
        HEADLESS = "headless"
        WINDOW_SIZE = "--window-size=1920x1080"

    def __init__(self, connection):
        self.connection = connection
        self.engine = connection.browser_type
        print(f"[BrowsingExecutor.__init__] Engine: {self.engine}")
        self.d = None
        self.blacklisted_extensions = self.connection.blacklisted_extensions if self.connection else []
        print(f"[BrowsingExecutor.__init__] Blacklisted extensions: {self.blacklisted_extensions}")
        self.whitelisted_extensions = self.connection.whitelisted_extensions if self.connection else []
        print(f"[BrowsingExecutor.__init__] Whitelisted extensions: {self.whitelisted_extensions}")
        try:
            mode = self.BrowsingModes.STANDARD
            if self.whitelisted_extensions != [] or self.blacklisted_extensions != []:
                if self.whitelisted_extensions:
                    mode = self.BrowsingModes.WHITELIST
                if self.blacklisted_extensions:
                    mode = self.BrowsingModes.BLACKLIST
            print(f"[BrowsingExecutor.__init__] Browsing mode: {mode}")
        except Exception as e:
            print(f"[BrowsingExecutor.__init__] Error occurred while setting the browsing mode: {str(e)}")
            mode = self.BrowsingModes.STANDARD
        try:
            self.mode = mode
            self.connect_c()
            print(f"[BrowsingExecutor.__init__] Connected to the driver.")
        except Exception as e:
            print(f"[BrowsingExecutor.__init__] Error occurred while connecting to the driver: {str(e)}")

    def act(self, action, **kwargs):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        try:
            transaction = LLMTransaction(
                organization=self.connection.assistant.organization,
                model=self.connection.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.BrowsingExecutor.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.BROWSING,
                is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            print(f"[BrowsingExecutor.act] Error occurred while creating the transaction: {str(e)}")

        if action == BrowserActionsNames.BROWSER_SEARCH:
            try:
                search_response, image_bytes = self.browser_search(kwargs["query"], kwargs["page"])
                print(f"[BrowsingExecutor.act] Search response: {search_response}")
            except Exception as e:
                print(f"[BrowsingExecutor.act] Error occurred while searching the query: {str(e)}")
                return None

            try:
                new_log_instance = self.connection.logs.create(
                    connection=self.connection,
                    action=action,
                    context_url=None,
                    html_content=None,
                    context_content=search_response,
                    log_content=f"Search query: {kwargs['query']} for the {kwargs['page']}th page of the {self.engine} "
                                f"search engine.",
                    screenshot=ContentFile(image_bytes, name=f"{uuid.uuid4()}.png")
                )
                new_log_instance.save()
                print(f"[BrowsingExecutor.act] Log instance created successfully.")
            except Exception as e:
                print(f"[BrowsingExecutor.act] Error occurred while saving the log: {str(e)}")
            return search_response
        elif action == BrowserActionsNames.CLICK_URL_IN_SEARCH:
            try:
                click_response, image_bytes = self.click_url_in_search(kwargs["search_results"], kwargs["click_url"])
                print(f"[BrowsingExecutor.act] Click response: {click_response}")
            except Exception as e:
                print(f"[BrowsingExecutor.act] Error occurred while clicking the URL in the search results: {str(e)}")
                return None

            try:
                new_log_instance = self.connection.logs.create(
                    connection=self.connection,
                    action=action,
                    context_url=kwargs["click_url"],
                    html_content=click_response,
                    context_content=None,
                    log_content=f"Clicked the URL: {kwargs['click_url']} in the search results.",
                    screenshot=ContentFile(image_bytes, name=f"{uuid.uuid4()}.png")
                )
                new_log_instance.save()
                print(f"[BrowsingExecutor.act] Log instance created successfully.")
            except Exception as e:
                print(f"[BrowsingExecutor.act] Error occurred while saving the log: {str(e)}")
            return click_response
        else:
            return f"[BrowsingExecutor.act] Invalid action: {action}. Must be one of {BrowserActionsNames.as_list()}."

    def connect_c(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument(BrowsingExecutor.BrowsingExecutorOptions.HEADLESS)  # Set headless mode
            options.add_argument(BrowsingExecutor.BrowsingExecutorOptions.WINDOW_SIZE)  # Set window size
            d = webdriver.Chrome(options=options)
            print(f"[BrowsingExecutor.connect_c] Connected to the driver.")
            self.d = d
        except Exception as e:
            return f"[BrowsingExecutor.connect_c] There has been an unexpected error while trying to connect to the driver: {e}"

    def close_c(self):
        try:
            self.d.quit()
            print(f"[BrowsingExecutor.close_c] Closed the driver.")
        except Exception as e:
            return f"[BrowsingExecutor.close_c] There has been an unexpected error while trying to close the driver: {e}"

    ##################################################

    def browser_search(self, query, page=1):
        if self.engine == SearchEnginesNames.GOOGLE:
            self.get_page(BrowserURLs.GOOGLE)
        else:
            return f"[BrowsingExecutor.browser_search] Invalid search engine: {self.engine}."
        search_input = self.find(FindByTypes.NAME, "q")
        print(f"[BrowsingExecutor.browser_search] Search input: {search_input}")
        try:
            self.send_keys(search_input, query)
            search_input.submit()
            print(f"[BrowsingExecutor.browser_search] Submitted the search query: {query}")
            self.wait()
        except Exception as e:
            return f"[BrowsingExecutor.browser_search] There has been an unexpected error while trying to search the query: {e}"
        # check the next page if needed
        if page > 1:
            try:
                next_page = self.find(FindByTypes.CSS_SELECTOR, "a#pnnext")
                self.click(next_page)
                print(f"[BrowsingExecutor.browser_search] Clicked the next page button.")
                self.wait()
            except Exception as e:
                return f"[BrowsingExecutor.browser_search] There has been an unexpected error while trying to go to the next page: {e}"
        return self.get_search_results()

    def get_page(self, url):
        try:
            self.d.get(url)
            print(f"[BrowsingExecutor.get_page] Got the url: {url}")
        except Exception as e:
            return f"[BrowsingExecutor.get_page] There has been an unexpected error while trying to get the url on browsing: {e}"

    def get_title(self):
        try:
            return self.d.title
        except Exception as e:
            return f"[BrowsingExecutor.get_title] There has been an unexpected error while trying to get the title on browsing: {e}"

    def get_page_content(self):
        try:
            clean_content = self.clean_page_content(self.d.page_source)
            print(f"[BrowsingExecutor.get_page_content] Got the page content.")
            return clean_content
        except Exception as e:
            return (
                f"[BrowsingExecutor.get_page_content] There has been an unexpected error while trying to get the content on browsing: {e}")

    def get_search_results(self):
        try:
            image_b64 = self.d.get_screenshot_as_base64()
            image_bytes = base64.b64decode(image_b64)
            print(f"[BrowsingExecutor.get_search_results] Got the screenshot.")
        except Exception as e:
            return (
                f"[BrowsingExecutor.get_search_results] There has been an unexpected error while trying to get the screenshot on browsing: {e}")
        try:
            raw_results = self.d.find_elements(By.CSS_SELECTOR, "div.g")
            clean_results = self.get_cleaned_search_results(raw_results)
            print(f"[BrowsingExecutor.get_search_results] Got the search results: {clean_results}")

            if self.mode == self.BrowsingModes.WHITELIST:
                clean_results = self.filter_on_whitelist(clean_results)
                print(f"[BrowsingExecutor.get_search_results] Filtered on whitelist: {clean_results}")
            elif self.mode == self.BrowsingModes.BLACKLIST:
                clean_results = self.filter_on_blacklist(clean_results)
                print(f"[BrowsingExecutor.get_search_results] Filtered on blacklist: {clean_results}")
            return clean_results, image_bytes
        except Exception as e:
            return (
                f"[BrowsingExecutor.get_search_results] There has been an unexpected error while trying to get the search results on browsing: {e}")

    def wait(self):
        try:
            time.sleep(IMPLICIT_WAIT_SECONDS)
            print(f"[BrowsingExecutor.wait] Waited for {IMPLICIT_WAIT_SECONDS} seconds.")
        except Exception as e:
            return f"[[BrowsingExecutor.wait] There has been an unexpected error while trying to wait on browsing: {e}"

    def find(self, by, query):
        try:
            if by not in FindByTypes.as_list():
                return f"[BrowsingExecutor.find] Invalid 'by' type: {by}. Must be one of {FindByTypes.as_list()}."
            return self.d.find_element(by=by, value=query)
        except Exception as e:
            return (
                f"[BrowsingExecutor.find] There has been an unexpected error while trying to find the element on browsing: {e}")

    def send_keys(self, element, text):
        try:
            element.send_keys(text)
            print(f"[BrowsingExecutor.send_keys] Sent keys: {text} to the element.")
        except Exception as e:
            return f"[BrowsingExecutor.send_keys] There has been an unexpected error while trying to send keys to the element on browsing: {e}"

    def click_url_in_search(self, search_results, click_url):
        try:
            for r in search_results:
                if r["url"] == click_url:
                    self.get_page(r["url"])
                    image_b64 = self.d.get_screenshot_as_base64()
                    image_bytes = base64.b64decode(image_b64)
                    print(f"[BrowsingExecutor.click_url_in_search] Retrieved the screenshot.")
                    content = self.get_page_content()
                    print(f"[BrowsingExecutor.click_url_in_search] Clicked the URL: {click_url}")
                    return content, image_bytes
            return f"[BrowsingExecutor.click_url_in_search] URL not found in search results: {click_url}"
        except Exception as e:
            return (
                f"[BrowsingExecutor.click_url_in_search] There has been an unexpected error while trying to click the URL in the "
                f"search results on browsing: {e}")

    def click(self, element):
        try:
            element.click()
            print(f"[BrowsingExecutor.click] Clicked the element.")
        except Exception as e:
            return f"[BrowsingExecutor.click] There has been an unexpected error while trying to click the element on browsing: {e}"

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
                print(f"[BrowsingExecutor.filter_on_whitelist] Error occurred while filtering on whitelist: {str(e)}")
        print(f"[BrowsingExecutor.filter_on_whitelist] Filtered results: {filtered_results}")
        return filtered_results

    def filter_on_blacklist(self, res):
        filtered_results = []
        for r in res:
            try:
                blacklisted = False
                # take the main domain
                r["url"] = r["url"].split("/")[2]
                for ext in self.blacklisted_extensions:
                    if r["url"].endswith(ext):
                        blacklisted = True
                        break
                if not blacklisted: filtered_results.append(r)
            except Exception as e:
                print(f"[BrowsingExecutor.filter_on_blacklist] Error occurred while filtering on blacklist: {str(e)}")
        print(f"[BrowsingExecutor.filter_on_blacklist] Filtered results: {filtered_results}")
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
                print(
                    f"[BrowsingExecutor.get_cleaned_search_results] Error occurred while cleaning the search results: {str(e)}")
        print(f"[BrowsingExecutor.get_cleaned_search_results] Cleaned results: {cleaned_results}")
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

        try:
            text = cleaner.clean_html(text)
            # remove the final html tag
            text = (text.replace("<div>", "").replace("</div>", "").replace("\n", "")
                    .replace("\t", ""))
            text = " ".join(text.split())
            print(f"[BrowsingExecutor.clean_page_content] Cleaned the page content.")
        except Exception as e:
            print(f"[BrowsingExecutor.clean_page_content] Error occurred while cleaning the page content: {str(e)}")
            return None
        return text
