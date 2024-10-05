#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:32
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
from .views import FrontPagesView


urlpatterns = [
    path(
        "front/landing/",
        FrontPagesView.as_view(template_name="landing_page.html"),
        name="landing-page",
    ),
    path(
        "front/pricing/",
        FrontPagesView.as_view(template_name="pricing_page.html"),
        name="pricing-page",
    ),
    path(
        "front/payment/",
        FrontPagesView.as_view(template_name="payment_page.html"),
        name="payment-page",
    ),
    path(
        "front/checkout/",
        FrontPagesView.as_view(template_name="checkout_page.html"),
        name="checkout-page",
    ),
    path(
        "front/help_center/",
        FrontPagesView.as_view(template_name="help_center_landing.html"),
        name="help-center-landing",
    ),
    path(
        "front/help_center/article/",
        FrontPagesView.as_view(template_name="help_center_article.html"),
        name="help-center-article",
    ),
]
