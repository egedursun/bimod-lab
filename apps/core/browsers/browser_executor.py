import logging
import time
import uuid
import re
import requests

from django.core.files.base import ContentFile
from lxml.html.clean import Cleaner

from apps.core.browsers.utils import (
    IMPLICIT_WAIT_SECONDS,
    SearchEnginesNames,
    FindByTypes,
    BrowserActionsNames,
    BrowsingModes,
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.datasource_browsers.utils import (
    BrowsingReadingAbilitiesNames
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from langchain_community.tools import (
    DuckDuckGoSearchResults
)

logger = logging.getLogger(__name__)


class BrowsingExecutor:

    def __init__(self, connection):
        self.connection = connection
        self.engine = connection.browser_type

        self.page_content = ""

        self.blacklisted_extensions = self.connection.blacklisted_extensions if self.connection else []
        self.whitelisted_extensions = self.connection.whitelisted_extensions if self.connection else []

        try:
            mode = BrowsingModes.STANDARD

            if self.whitelisted_extensions or self.blacklisted_extensions:
                if self.whitelisted_extensions:
                    mode = BrowsingModes.WHITELIST
                if self.blacklisted_extensions:
                    mode = BrowsingModes.BLACKLIST

        except Exception as e:
            mode = BrowsingModes.STANDARD
            logger.error(f"Error while setting browsing mode, setting to standard: {str(e)}")
        try:
            self.mode = mode
            logger.info("Initialized duckduckgo-based browsing executor.")

        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            pass

    def act(self, action, **kwargs):
        try:
            logger.info(f"LLM Transaction created for browsing action: {action}.")

        except Exception as e:
            logger.error(f"Error while creating LLM Transaction for browsing action: {str(e)}")
            pass

        try:
            tx = LLMTransaction(
                organization=self.connection.assistant.organization,
                model=self.connection.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.BROWSING,
                is_tool_cost=True,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )

            tx.save()

            logger.info(f"LLM Transaction created for browsing action: {action}.")

        except Exception as e:
            logger.error(f"Error while creating LLM Transaction for browsing action: {str(e)}")
            pass

        if action == BrowserActionsNames.BROWSER_SEARCH:
            try:
                search_output, image_bytes = self.browser_search(
                    kwargs["query"],
                    kwargs["page"]
                )

                logger.info(f"Search query: {kwargs['query']} for the {kwargs['page']}th page using DuckDuckGo.")
                print("[SEARCH OUTPUT] \n =========== \n", search_output, "\n =========== \n\n")

            except Exception as e:
                logger.error(f"Error while searching the query: {str(e)}")
                return None

            try:

                new_log_instance = self.connection.logs.create(
                    connection=self.connection,
                    action=action,
                    context_url=None,
                    html_content=None,
                    context_content=search_output,
                    log_content=f"Search query: {kwargs['query']} for the {kwargs['page']}th page of the {self.engine}"
                                f"search engine.",
                    screenshot=ContentFile(
                        image_bytes,
                        name=f"{uuid.uuid4()}.png"
                    )
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
                click_response, image_bytes = self.click_url_in_search(
                    kwargs["search_results"],
                    kwargs["click_url"]
                )

                logger.info(f"Clicked the URL: {kwargs['click_url']} in the search results.")
                print("[CLICK RESPONSE] \n =========== \n", click_response, "\n =========== \n\n")

            except Exception as e:
                logger.error(f"Error while clicking the URL in the search results: {str(e)}")

                return None

            try:
                logger.info(f"Log instance created for clicking URL: {kwargs['click_url']}.")

            except Exception as e:
                logger.error(f"Error while creating log instance for click: {str(e)}")
                pass

            return click_response

        else:
            logger.error(f"Invalid action: {action}. Must be one of {BrowserActionsNames.as_list()}.")

            return f"[BrowsingExecutor.act] Invalid action: {action}. Must be one of {BrowserActionsNames.as_list()}."

    def browser_search(self, query, page=1):
        try:
            tool = DuckDuckGoSearchResults(
                max_results=page,
                output_format="list"
            )

            raw_results = tool.run(query)

            cleaned = self.get_cleaned_search_results(
                raw_results
            ) if isinstance(
                raw_results,
                list
            ) else raw_results

            return cleaned, None

        except Exception as e:
            logger.error(f"Error during DuckDuckGo search: {str(e)}")

            return f"[BrowsingExecutor.browser_search] Error: {e}", None

    def click_url_in_search(
        self,
        search_results,
        click_url
    ):

        for r in search_results:
            if r.get("url") == click_url:
                try:
                    response = requests.get(click_url)
                    html_content = response.text

                    clean_content = self.clean_page_content(
                        html_content
                    )

                    print(f"Clicked the URL: {click_url} and fetched content.")
                    return clean_content, None

                except Exception as e:
                    logger.error(f"Error while fetching URL content: {str(e)}")

                    return f"[BrowsingExecutor.click_url_in_search] Error: {e}"

        return f"[BrowsingExecutor.click_url_in_search] URL not found in search results: {click_url}"

    def get_page(self, url):
        try:
            response = requests.get(url)
            self.page_content = response.text

            print(f"Opened the URL: {url} on browsing executor.")

        except Exception as e:
            logger.error(f"Error while opening URL: {str(e)}")

            return f"[BrowsingExecutor.get_page] Error: {e}"

    def get_title(self):
        try:
            print("Getting the title of the page.")
            match = re.search(r'<title>(.*?)</title>', self.page_content, re.IGNORECASE | re.DOTALL)
            title = match.group(1).strip() if match else "No title found"

            return title

        except Exception as e:
            logger.error(f"Error while getting title: {str(e)}")

            return f"[BrowsingExecutor.get_title] Error: {e}"

    def get_page_content(self):
        try:
            print("[RAW PAGE CONTENT] \n =========== \n", self.page_content, "\n =========== \n\n")

            clean_content = self.clean_page_content(
                self.page_content
            )

            print("Returning cleaned page content.")
            print("[CLEANED PAGE CONTENT] \n =========== \n", clean_content, "\n =========== \n\n")

            return clean_content

        except Exception as e:
            logger.error(f"Error while getting page content: {str(e)}")

            return f"[BrowsingExecutor.get_page_content] Error: {e}"

    def get_search_results(self):
        return self.browser_search("", page=1)

    def wait(self):
        try:
            time.sleep(IMPLICIT_WAIT_SECONDS)

            print("Waiting on browsing executor.")

        except Exception as e:
            logger.error(f"Error during wait: {str(e)}")

            return f"[BrowsingExecutor.wait] Error: {e}"

    def find(self, by, query):
        try:
            if by not in FindByTypes.as_list():
                return f"[BrowsingExecutor.find] Invalid 'by' type: {by}. Must be one of {FindByTypes.as_list()}."

            print("Simulated finding of element on page.")

            if query in self.page_content:
                return query

            else:
                return None

        except Exception as e:
            logger.error(f"Error in find: {str(e)}")

            return f"[BrowsingExecutor.find] Error: {e}"

    def send_keys(self, element, text):
        try:
            print("Simulated sending keys to element on browsing.")

        except Exception as e:
            logger.error(f"Error in send_keys: {str(e)}")

            return f"[BrowsingExecutor.send_keys] Error: {e}"

    def click(self, element):
        try:
            print("Simulated click on element on browsing.")

        except Exception as e:
            logger.error(f"Error in click: {str(e)}")

            return f"[BrowsingExecutor.click] Error: {e}"

    def filter_on_whitelist(self, res):
        filtered_results = []

        for r in res:
            try:

                domain = r.get("url", "").split("/")[2] if "url" in r and r["url"] else ""

                for ext in self.whitelisted_extensions:
                    if domain.endswith(ext):
                        filtered_results.append(r)
                        break

            except Exception as e:
                logger.error(f"Error while filtering on whitelist: {str(e)}")
                pass

        print("Filtered results on whitelist:", filtered_results)

        return filtered_results

    def filter_on_blacklist(self, res):
        filtered_results = []

        for r in res:
            try:
                domain = r.get("url", "").split("/")[2] if "url" in r and r["url"] else ""
                blacklisted = False

                for ext in self.blacklisted_extensions:
                    if domain.endswith(ext):
                        blacklisted = True
                        break

                if not blacklisted:
                    filtered_results.append(r)

            except Exception as e:
                logger.error(f"Error while filtering on blacklist: {str(e)}")
                pass

        print("Filtered results on blacklist:", filtered_results)

        return filtered_results

    def get_cleaned_search_results(self, raw_results):

        if not isinstance(raw_results, list):

            try:
                import json
                raw_results = json.loads(raw_results)

            except Exception as e:
                logger.error(f"Error parsing raw search results: {str(e)}")

                return raw_results

        cleaned_results = []

        for r in raw_results:
            try:
                clean = {}
                clean["url"] = r.get("link", "")
                clean["title"] = r.get("title", "")
                clean["snippet"] = r.get("snippet", "")

                cleaned_results.append(clean)

            except Exception as e:
                logger.error(f"Error cleaning search result: {str(e)}")
                pass

        print("Cleaned search results:", cleaned_results)

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

            text = (
                text.replace("<div>", "")
                .replace("</div>", "")
                .replace("\n", "")
                .replace("\t", "")
            )

            text = " ".join(text.split())

            print("[HTML PAGE CONTENT] \n =========== \n", text, "\n =========== \n\n")
            print("Cleaned the page content.")

        except Exception as e:
            logger.error(f"Error while cleaning the page content: {str(e)}")

            return None

        return text


if __name__ == "__main__":
    class Connection:
        def __init__(self):
            self.browser_type = SearchEnginesNames.GOOGLE
            self.blacklisted_extensions = []
            self.whitelisted_extensions = []

            self.reading_abilities = {
                BrowsingReadingAbilitiesNames.JAVASCRIPT: False,
                BrowsingReadingAbilitiesNames.STYLE: False,
                BrowsingReadingAbilitiesNames.COMMENTS: False,
                BrowsingReadingAbilitiesNames.LINKS: False,
                BrowsingReadingAbilitiesNames.META: False,
                BrowsingReadingAbilitiesNames.PAGE_STRUCTURE: False,
                BrowsingReadingAbilitiesNames.PROCESSING_INSTRUCTIONS: False,
                BrowsingReadingAbilitiesNames.FRAMES: False,
                BrowsingReadingAbilitiesNames.FORMS: False,
                BrowsingReadingAbilitiesNames.EMBEDDED: False,
                BrowsingReadingAbilitiesNames.REMOVE_TAGS: False
            }
            self.logs = []


    connection = Connection()
    be = BrowsingExecutor(connection)

    result = be.act(
        BrowserActionsNames.BROWSER_SEARCH,
        query="Bimod.io",
        page=1
    )

    print(result)

    result = be.act(
        BrowserActionsNames.CLICK_URL_IN_SEARCH,
        search_results=result,
        click_url=result[0]["url"]
    )

    print(result)

    pass
