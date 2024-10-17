#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:31
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
from .views import (
    CollapsedMenuView,
    ContentNavSidebarView,
    VerticalView,
    HorizontalView,
    WithoutMenuView,
    WithoutNavView,
    FluidView,
    ContainerView,
    BlankView,
)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "layouts/collapsed_menu/",
        login_required(CollapsedMenuView.as_view(template_name="layouts_collapsed_menu.html")),
        name="layouts-collapsed-menu",
    ),
    path(
        "layouts/content_navbar/",
        login_required(VerticalView.as_view(template_name="layouts_content_navbar.html")),
        name="layouts-content-navbar",
    ),
    path(
        "layouts/content_nav_sidebar/",
        login_required(ContentNavSidebarView.as_view(template_name="layouts_content_navbar_with_sidebar.html")),
        name="layouts-content-nav-sidebar",
    ),
    path(
        "layouts/horizontal/",
        login_required(HorizontalView.as_view(template_name="layouts_horizontal.html")),
        name="layouts-horizontal",
    ),
    path(
        "layouts/without_menu/",
        login_required(WithoutMenuView.as_view(template_name="layouts_without_menu.html")),
        name="layouts-without-menu",
    ),
    path(
        "layouts/without_navbar/",
        login_required(WithoutNavView.as_view(template_name="layouts_without_navbar.html")),
        name="layouts-without-navbar",
    ),
    path(
        "layouts/fluid/",
        login_required(FluidView.as_view(template_name="layouts_fluid.html")),
        name="layouts-fluid",
    ),
    path(
        "layouts/container/",
        login_required(ContainerView.as_view(template_name="layouts_container.html")),
        name="layouts-container",
    ),
    path(
        "layouts/blank/",
        login_required(BlankView.as_view(template_name="layouts_blank.html")),
        name="layouts-blank",
    ),
]
