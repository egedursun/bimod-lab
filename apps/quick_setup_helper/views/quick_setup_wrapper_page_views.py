#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: quick_setup_wrapper_page_views.py
#  Last Modified: 2024-11-19 16:24:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-19 16:24:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import TemplateView

from apps.datasource_file_systems.utils import (
    DATASOURCE_FILE_SYSTEMS_OS_TYPES
)

from apps.datasource_nosql.utils import (
    NOSQL_DATABASE_CHOICES
)

from apps.datasource_sql.utils import (
    DBMS_CHOICES
)

from web_project import TemplateLayout


class QuickSetupHelperView_QuickSetupWrapperPage(
    LoginRequiredMixin,
    TemplateView
):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        sql_dbms_choices = DBMS_CHOICES
        nosql_dbms_choices = NOSQL_DATABASE_CHOICES
        file_system_os_choices = DATASOURCE_FILE_SYSTEMS_OS_TYPES

        context['sql_dbms_choices'] = sql_dbms_choices
        context['nosql_dbms_choices'] = nosql_dbms_choices
        context['file_system_os_choices'] = file_system_os_choices

        return context
