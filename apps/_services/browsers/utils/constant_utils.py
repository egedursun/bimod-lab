#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: constant_utils.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: constant_utils.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:01:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
