#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-11-02 19:21:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 19:21:22
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
import secrets

from apps.slider.models import SliderGoogleAppsConnection
from apps.slider.utils import SLIDER_GOOGLE_APPS_CONNECTION_API_KEY_DEFAULT_LENGTH

logger = logging.getLogger(__name__)


def generate_google_apps_connection_api_key():
    return secrets.token_urlsafe(SLIDER_GOOGLE_APPS_CONNECTION_API_KEY_DEFAULT_LENGTH)


def is_valid_google_apps_authentication_key(authentication_key: str):
    connection_object = SliderGoogleAppsConnection.objects.filter(connection_api_key=authentication_key).first()
    if not connection_object:
        logger.error(f"Google Apps Authentication Key: {authentication_key} is not valid.")
    return connection_object
