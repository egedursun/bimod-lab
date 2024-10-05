#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.urls import path
from .views import WizardExamplesView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "wizard_ex/checkout/",
        login_required(WizardExamplesView.as_view(template_name="wizard_ex_checkout.html")),
        name="wizard-ex-checkout",
    ),
    path(
        "wizard_ex/property_listing/",
        login_required(WizardExamplesView.as_view(template_name="wizard_ex_property_listing.html")),
        name="wizard-ex-property-listing",
    ),
    path(
        "wizard_ex/create_deal/",
        login_required(WizardExamplesView.as_view(template_name="wizard_ex_create_deal.html")),
        name="wizard-ex-create-deal",
    ),
]
