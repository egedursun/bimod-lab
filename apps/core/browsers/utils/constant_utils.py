#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
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
#
#

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


class BrowsingModes:
    STANDARD = "standard"
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"


class BrowsingExecutorOptions:
    HEADLESS = "headless"
    WINDOW_SIZE = "--window-size=1920x1080"
