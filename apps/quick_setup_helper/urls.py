#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-18 20:18:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:18:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.urls import path

from apps.quick_setup_helper.views import QuickSetupHelperView_QuickSetupManager
from apps.quick_setup_helper.views import QuickSetupHelperView_QuickSetupWrapperPage

app_name = 'quick_setup_helper'

urlpatterns = [
    path("", QuickSetupHelperView_QuickSetupWrapperPage.as_view(
        template_name="quick_setup_helper/quick_setup_wrapper_page.html"
    ), name="wrapper"),
    path("execute/", QuickSetupHelperView_QuickSetupManager.as_view(), name="execute"),
]
