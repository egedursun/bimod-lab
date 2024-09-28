from selenium.webdriver.common.by import By

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


class BrowserActionsNames:
    BROWSER_SEARCH = "browser_search"
    CLICK_URL_IN_SEARCH = "click_url_in_search"

    @staticmethod
    def as_list():
        return [BrowserActionsNames.BROWSER_SEARCH, BrowserActionsNames.CLICK_URL_IN_SEARCH]
